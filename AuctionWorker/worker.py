from datetime import datetime
from celery import Celery, shared_task
from flask import jsonify
import requests
from python_json_config import ConfigBuilder

config = builder.parse_config('/app/config.json')

worker = Celery('auction_worker',
                    broker='amap://admin:mypass@rabbit:5672', 
                    backend=' rpc://')

@worker.task
def end_auction(auctionId):
    ## set the auction to be closed
    ## give the money back to the users
    ## give the gacha to the user who won
    ## delete the gacha from the user who auctioned it
    ## give the money to the user who auctioned it
    auction = requests.get(config.dbmanagers.auction + f'/auction/{auctionId}').json()
    if auction is None or auction['status'] > 1: # if the auction is already been closed returns
        return;

    auction['status'] = 2
    requests.put(config.dbmanagers.auction + f'/auction/{auctionId}', json=jsonify(auction))

    # get the winning bid
    bids = requests.get(config.dbmanagers.auction + f'/auctionbid/auction/{auctionId}').json()

    winningBid = {
        "id": None,
        "userId": None,
        "bidAmount": -100,
        "auctionId": None,
        "timestamp": None
    }

    for bid in bids:
        if bid['bidAmount'] > winningBid['bidAmount']:
            winningBid = bid

    transaction = {
        "sellerId":auction['userId'], 
        'buyerId':winningBid['userId'],
        'auctionBidId':winningBid['id'], 
        'timestamp': datetime.now()
    }
    
    #
    resp = requests.post(config.dbmanagers.transaction + f'/auctiontransaction', json=jsonify(transaction))
    if resp.status_code != 200: return
    

    ## return money to the ones that have lost
    for bid in bids:
        if bid['id'] != winningBid['id']:
            resp = requests.put(config.services.paymentsuser + f'/api/player/currency/increase/{bid['userId']}', json=jsonify({"amount": bid['bidAmount']}))
            if resp.status_code!= 200: print(f"Something went wrong INCREASE : {bid['userId']}")

    # give money to the winning bidder
    requests.put(config.services.paymentsuser + f'/api/player/currency/increase/{auction['userId']}', json=jsonify({"amount": winningBid['bidAmount']}))

    ##GET GACHA

    gacha = requests.get(config.services.gachauser + f'/api/player/gacha/player-collection/item/<int:collectionId>/{auction['gachaCollectionId']}')
    ## Give gacha to user
    requests.post(
        f'{config.dbmanagers.gacha}/gachacollection', 
        json={
            "gachaId":auction['id'],
            "userId":winningBid['buyerId'],
            "source":f"{auction['id']}"
        }
    )

    ## remove gacha from seller user
    requests.delete(config.dbmanagers.gacha + f'/gachacollection/{auction['gachaCollectionId']}')

    requests.put(config.dbmanagers.transaction + f'/auctiontransaction', json=jsonify(transaction))
    
    print(f"FINISHED -> {auctionId}")