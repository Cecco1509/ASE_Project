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
credentials = builder.parse_config('/run/secrets/auctioneer_credentials')

def checker():

    ## authentication
    auth_res = requests.post(f"{config.services.authmicroservice}/api/admin/login", json={
        "username": credentials.username,
        "password": credentials.password
    }, verify=False)

    if auth_res.status_code != 200:
        print("Authentication failed")
        return
    
    data = auth_res.json()
    jwt_token = data['token']
    headers = {
        "Authorization": f"Bearer {jwt_token}",
    }

    body = {
        "auctionStart" : None,
        "auctionEnd" : None,
        "status" : "PASSED"
    }

    while True:
        now : datetime = datetime.now()
        print(f"Current time: {now.strftime('%d/%m/%Y, %H:%M:%S')}")

        response = requests.get(f"{config.dbmanagers.auction}/auction/status/ACTIVE", verify=False)
        print("CHECKING FOR ACTIVE AUCTIONS ", now)
        if response.status_code == 200:
            auctions = response.json()
            for auction in auctions:
                if datetime.strptime(auction['auctionEnd'], "%a, %d %b %Y %H:%M:%S %Z") <= now and auction['status'] == 'ACTIVE':
                    res = requests.put(f"{config.services.auction}/api/admin/auction/{auction["id"]}", headers=headers, json=body, verify=False)
                    print(f"END AUCTION {auction["id"]} -> RESPONSE {res.status_code}")
        
        now = datetime.now()
        print(f"Sleeping for {60 - now.second} seconds")  # Sleep until next minute start.
        sleep(60-now.second)


if __name__ == '__main__':
    print("Starting")
    checker()