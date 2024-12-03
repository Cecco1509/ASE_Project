import functools
from time import sleep
import requests
from celery import Celery
from argparse import ArgumentParser
from python_json_config import ConfigBuilder
from datetime import datetime
from worker import end_auction
import pytz

print = functools.partial(print, flush=True)

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

celery_app = Celery('worker',
                    broker='amqp://admin:mypass@rabbit:5672', 
                    backend='rpc://')

def checker():

    tz = pytz.timezone('Europe/Rome')

    while True:
        now : datetime = datetime.now(tz=tz)
        print(f"Current time: {now.strftime('%d/%m/%Y, %H:%M:%S')}")

        response = requests.get(f"{config.dbmanagers.auction}/auction/status/ACTIVE")
        print("CHECKING FOR ACTIVE AUCTIONS", now)
        if response.status_code == 200:
            auctions = response.json()
            for auction in auctions:
                if tz.localize(datetime.strptime(auction['auctionEnd'], "%a, %d %b %Y %H:%M:%S %Z")) <= now and auction['status'] == 'ACTIVE':
                    end_auction.delay(auction['id'])
                    print(f"Auction {auction['id']} sendend")
        
        now = datetime.now()
        print(f"Sleeping for {60 - now.second} seconds")  # Sleep until next minute start.
        sleep(60-now.second)


if __name__ == '__main__':
    print("Starting")
    checker()