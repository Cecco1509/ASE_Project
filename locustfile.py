from datetime import datetime, timedelta
import random
from locust import HttpUser, task, between

# class GachaMicroserviceTasks(HttpUser):
#     """Tasks for Gacha microservice endpoints."""
#     wait_time = between(1, 5)
#     def on_start(self):
#     # You can also do it only the first time using «if self.token:»
#         response = self.client.post("/api/player/register",json={"username": "user1234", "password": "password1"}, verify=False)
#         response = self.client.post("/api/player/login",json={"username": "user1234", "password": "password1"}, verify=False)
#         if response.status_code == 200:
#             self.token = response.json().get("Access token")
#             print("Access token obtained successfully.")
#         else:
#             self.token = None
#             print(f"Failed to obtain token: {response.status_code}, {response.text}")


#     @task
#     def get_player_collection(self):
#         if self.token:
#             user_id = 1  # Fiksni ID
#             headers = {"Authorization": f"Bearer {self.token}"}      
#             self.client.get(f"/api/player/gacha/player-collection", headers=headers, verify=False)

#     @task
#     def get_collection_item_details(self):
#         if self.token:
#             collection_id = 1  # Fiksni ID
#             headers = {"Authorization": f"Bearer {self.token}"}
#             self.client.get(f"/api/player/gacha/player-collection/item/{collection_id}", headers=headers, verify=False)

#     @task
#     def get_gacha_details(self):
#         if self.token:
#             gacha_id = 1  # Fiksni ID
#             headers = {"Authorization": f"Bearer {self.token}"}
#             self.client.get(f"/api/player/gacha/player-collection/gacha/{gacha_id}", headers=headers, verify=False)

#     @task
#     def get_system_gacha_collection(self):
#         if self.token:
#             headers = {"Authorization": f"Bearer {self.token}"}
#             self.client.get("/api/player/gacha/system-collection", headers=headers, verify=False)

#     @task
#     def get_system_gacha_details(self):
#         if self.token:
#             gacha_id = 1  # Fiksni ID
#             headers = {"Authorization": f"Bearer {self.token}"}
#             self.client.get(f"/api/player/gacha/system-collection/{gacha_id}", headers=headers, verify=False)
#     @task
#     def roll_gacha(self):
#         if self.token:
#             headers = {"Authorization": f"Bearer {self.token}"}
#             self.client.post("/api/player/gacha/roll", headers=headers, verify=False, json={"rarity_level": "Common"})


class AuctionMicroserviceTasks(HttpUser):
    """Tasks for Gacha microservice endpoints."""
    wait_time = between(1, 10)
    def on_start(self):
    # You can also do it only the first time using «if self.token:
        random_number = random.randint(1, 9999999)

# Format the number as a zero-padded 7-digit string
        user_code = f"{random_number:07}"

        response = self.client.post("/api/player/register",json={"username": f"user{user_code}", "password": "password1", "profilePicture" : "random"}, verify=False)
        id = response.json()["userId"]
        response = self.client.post("/api/player/login",json={"username": f"user{user_code}", "password": "password1"}, verify=False)
        if response.status_code == 200:
            self.token = response.json().get("Access token")
            headers = {
                "Authorization": f"Bearer {self.token}"
            }
            res = self.client.put(f"/api/player/increase/{id}",json={"amount" : 40000000}, headers=headers ,verify=False)
            print(f"\n############## Increase response: {res.status_code}, {res.text}\n")
            print("Access token obtained successfully.")
        else:
            self.token = None
            print(f"Failed to obtain token: {response.status_code}, {response.text}")

    @task
    def get_active_auctions(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}      
            self.client.get(f"/api/player/auction/market", headers=headers, verify=False)

    @task
    def bid_auction(self):
        if self.token:
            auction_id = 0
            headers = {"Authorization": f"Bearer {self.token}"}
            market_res = self.client.get(f"/api/player/auction/market", headers=headers, verify=False)
            market = market_res.json()["market"]
            random_number = random.randint(1, 999)
            if len(market) > 0:
                auction = market[random.randint(0, len(market)-1)]
                auction_id = auction["auctionId"]
                self.client.post(f"/api/player/auction/bid/{auction_id}", headers=headers, verify=False, json={"bidAmount": random_number})

    @task
    def post_auction(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            gachaColl_res = self.client.post("/api/player/gacha/roll", headers=headers, verify=False, json={"rarity_level": "Common"})
            gachaCollId = gachaColl_res.json()["collectionId"]
            self.client.post(f"/api/player/auction/create", headers=headers, verify=False, json={
                "auctionStart" : (datetime.now()).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "auctionEnd" : (datetime.now() + timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "minimumBid" : 30,
                "gachaCollectionId" : gachaCollId
            })

    def on_stop(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.post("/api/player/logout", headers=headers, verify=False)
            self.client.delete("/api/player/delete", headers=headers, verify=False)
