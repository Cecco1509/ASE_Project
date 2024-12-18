import functools
from time import sleep
import requests
from python_json_config import ConfigBuilder
from datetime import datetime

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

print = functools.partial(print, flush=True)

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
credentials = builder.parse_config('/run/secrets/auctioneer_credentials')

def checker():

    authenticated = False

    while not authenticated:
    ## authentication
        try:
            auth_res = requests.post(f"{config.services.authmicroservice}/api/admin/login", json={
                "username": credentials.username,
                "password": credentials.password
            }, verify=False, timeout=config.timeout.medium)

            auth_res.raise_for_status()
            authenticated = True
        except Exception as e:
            print("Error while connecting to auth microservice: ", e)
            sleep(10)
            continue
    
    data = auth_res.json()
    jwt_token = data['Access token']
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

        try:
            response = requests.get(f"{config.dbmanagers.auction}/auction/status/ACTIVE", verify=False, timeout=config.timeout.medium)
            response.raise_for_status()
            print("CHECKING FOR ACTIVE AUCTIONS ", now)
            if response.status_code == 200:
                auctions = response.json()
                for auction in auctions:
                    if datetime.strptime(auction['auctionEnd'], "%a, %d %b %Y %H:%M:%S %Z") <= now and auction['status'] == 'ACTIVE':
                        res = requests.put(f"{config.services.auction}/api/admin/auction/{auction["id"]}", headers=headers, json=body, verify=False, timeout=config.timeout.medium)
                        print(f"END AUCTION {auction["id"]} -> RESPONSE {res.status_code}")
        except Exception as e:
            print("Error while accessing the auctiondbmanager: ", e)

        now = datetime.now()
        print(f"Sleeping for {60 - now.second} seconds")  # Sleep until next minute start.
        sleep(60-now.second)


if __name__ == '__main__':
    print("Starting")
    checker()