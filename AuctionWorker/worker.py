from datetime import datetime
from celery import Celery, shared_task
from flask import jsonify
import requests
from python_json_config import ConfigBuilder

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

worker = Celery('auction_worker',
                    broker='amap://admin:mypass@rabbit:5672', 
                    backend=' rpc://')

@worker.task
def end_auction(auctionId):
    # Fetch auction details
    auction = requests.get(f"{config.dbmanagers.auction}/auction/{auctionId}").json()
    if not auction or auction['status'] > 1:  # Auction already closed
        return

    # Close the auction
    auction['status'] = 2
    requests.put(f"{config.dbmanagers.auction}/auction/{auctionId}", json=auction)

    # Get all bids for the auction
    bids = requests.get(f"{config.dbmanagers.auction}/auctionbid/auction/{auctionId}").json()
    if not bids:
        return

    # Find the winning bid
    winningBid = max(bids, key=lambda bid: bid['bidAmount'])

    # Create a transaction
    transaction = {
        "sellerId": auction['userId'],
        "buyerId": winningBid['userId'],
        "auctionBidId": winningBid['id'],
        "timestamp": datetime.now().isoformat()
    }

    resp = requests.post(f"{config.dbmanagers.transaction}/auctiontransaction", json=transaction)
    if resp.status_code != 200:
        return

    # Return money to losing bidders
    for bid in bids:
        if bid['id'] != winningBid['id']:
            resp = requests.put(
                f"{config.services.paymentsuser}/api/player/currency/increase/{bid['userId']}",
                json={"amount": bid['bidAmount']}
            )
            if resp.status_code != 200:
                print(f"Error returning money to user {bid['userId']}")

    # Give money to the seller
    requests.put(
        f"{config.services.paymentsuser}/api/player/currency/increase/{auction['userId']}",
        json={"amount": winningBid['bidAmount']}
    )

    # Fetch Gacha
    gacha = requests.get(
        f"{config.services.gachauser}/api/player/gacha/player-collection/item/{auction['gachaCollectionId']}"
    ).json()

    # Assign Gacha to the winning bidder
    requests.post(
        f"{config.dbmanagers.gacha}/gachacollection",
        json={
            "gachaId": auction['id'],
            "userId": winningBid['userId'],
            "source": f"{auction['id']}"
        }
    )

    # Remove Gacha from the seller
    requests.delete(f"{config.dbmanagers.gacha}/gachacollection/{auction['gachaCollectionId']}")

    # Update the transaction (if required)
    requests.put(f"{config.dbmanagers.transaction}/auctiontransaction", json=transaction)

    print(f"FINISHED -> {auctionId}")