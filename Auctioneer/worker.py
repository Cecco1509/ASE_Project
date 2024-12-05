from datetime import datetime
from celery import Celery, shared_task
from celery.contrib.abortable import AbortableTask
import requests
from python_json_config import ConfigBuilder

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

celery_app = Celery('worker',
                    broker='amqp://admin:mypass@rabbit:5672', 
                    backend='rpc://')

#@shared_task(bind=True, base=AbortableTask)
@celery_app.task
def end_auction(auctionId):
    # Fetch auction details
    print("Started auctioneer process", flush=True)

    response = requests.get(f"{config.dbmanagers.auction}/auction/{auctionId}")
    auction_data = response.json()

    auction = requests.get(f"{config.dbmanagers.auction}/auction/{auctionId}")

    if auction.status_code == 404: 
        print("Auction not found", flush=True)
        exit(1)

    try:
        auction = auction.json()
        print(auction, flush=True)
    except Exception as e:
        print("Failed decode auction", flush=True)
        exit(1)

    if not auction or auction['status'] != "ACTIVE":  # Auction already closed
        print("Auction already closed", flush=True)
        exit(1)

    # Close the auction
    auction['status'] = "PASSED"
    start = datetime.strptime(auction['auctionStart'], "%a, %d %b %Y %H:%M:%S %Z")
    end = datetime.strptime(auction['auctionEnd'], "%a, %d %b %Y %H:%M:%S %Z")
    timestamp = datetime.strptime(auction['timestamp'], "%a, %d %b %Y %H:%M:%S %Z")

    auction['auctionStart'] = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    auction['auctionEnd'] = end.strftime("%Y-%m-%dT%H:%M:%SZ")
    auction['timestamp'] = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")

    print(auction, flush=True)
    print("START AFTER STRF"+start.strftime("%Y-%m-%dT%H:%M:%SZ"), flush=True)

    print("TRY SET TO PASSED", flush=True)

    requests.put(f"{config.dbmanagers.auction}/auction/{auctionId}", json=auction)

    print("SET TO PASSED", flush=True)

    # Get all bids for the auction
    bids = requests.get(f"{config.dbmanagers.auction}/auctionbid/auction/{auctionId}").json()
    if not bids:
        print("No bids for the auction", flush=True)
        exit(1)

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
        exit(1)

    resp = requests.patch(f"{config.dbmanagers.user}/user/{auction['userId']}",
                        json={"ingameCurrency": float(winningBid['bidAmount'])}
                    )

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

    return