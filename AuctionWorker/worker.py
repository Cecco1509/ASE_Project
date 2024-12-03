from datetime import datetime
from celery import Celery, shared_task
from celery.contrib.abortable import AbortableTask
import requests
from python_json_config import ConfigBuilder
import pytz

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

celery_app = Celery('worker',
                    broker='amqp://admin:mypass@rabbit:5672', 
                    backend='rpc://')

#@shared_task(bind=True, base=AbortableTask)
@celery_app.task
def end_auction(auctionId):
    # Fetch auction details
    print("PARTITOOOOOOOOO ", flush=True)
    tz = pytz.timezone("Europe/Rome")

    response = requests.get(f"{config.dbmanagers.auction}/auction/{auctionId}")

    if response.status_code == 404: 
        print("Auction not found", flush=True)
        return

    try:
        auction = response.json()
        print(auction, flush=True)
    except Exception as e:
        print("Failed decode auction", flush=True)
        return

    if not auction or auction['status'] != "ACTIVE":  # Auction already closed
        print("Auction already closed", flush=True)
        return

    # Close the auction
    auction['status'] = "PASSED"
    start = datetime.strptime(auction['auctionStart'], "%a, %d %b %Y %H:%M:%S %Z")
    end = datetime.strptime(auction['auctionEnd'], "%a, %d %b %Y %H:%M:%S %Z")
    timestamp = datetime.strptime(auction['timestamp'], "%a, %d %b %Y %H:%M:%S %Z")

    auction['auctionStart'] = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    auction['auctionEnd'] = end.strftime("%Y-%m-%dT%H:%M:%SZ")
    auction['timestamp'] = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")


    try:
        requests.put(f"{config.dbmanagers.auction}/auction/{auctionId}", json=auction)
    except Exception as e:
        print("Failed updating auction", flush=True)
        return

    print("SET TO PASSED", flush=True)

    # Get all bids for the auction
    try:
        bids_req = requests.get(f"{config.dbmanagers.auction}/auctionbid/auction/{auctionId}")
        bids_req.raise_for_status()
        bids = bids_req.json()
    except Exception as e:
        print("Failed loading bids", flush=True)
        return
    
    if len(bids) == 0:
        print("No bids found, no work has to be done", flush=True)
        return

    # Find the winning bid
    winningBid = max(bids, key=lambda bid: bid['bidAmount'])

    print("Winning bid -> ",winningBid, flush=True)

    # Create a transaction
    transaction = {
        "sellerId": auction['userId'],
        "buyerId": winningBid['userId'],
        "auctionBidId": winningBid['id'],
        "timestamp": datetime.now(tz=tz).strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    print("Transaction -> ", transaction, flush=True)

    try:
        resp = requests.post(f"{config.dbmanagers.transaction}/auctiontransaction", json=transaction)
        resp.raise_for_status()
    except Exception as e:
        print("Failed creating transaction", flush=True)
        return

    try:
        resp = requests.patch(f"{config.dbmanagers.user}/user/{auction['userId']}",
                            json={"ingameCurrency": float(winningBid['bidAmount'])}
                        )
    except Exception as e:
        print("Failed assign money", flush=True)
        return
    
    # Assign Gacha to the winning bidder
    try:
        coll_res = requests.get(f"{config.dbmanagers.gacha}/gachacollection/item/{auction['gachaCollectionId']}")
        gacha_coll = coll_res.json()

        res = requests.put(
            f"{config.dbmanagers.gacha}/gachacollection/{auction['gachaCollectionId']}",
            json={
                "gachaId": gacha_coll['gachaId'],
                "userId": winningBid['userId'],
                "source": "AUCTION"
            }
        )
        res.raise_for_status()
    except Exception as e:
        print("Failed assign gacha: "+str(e), flush=True)
        return

    print(f"FINISHED -> {auctionId}")

    return