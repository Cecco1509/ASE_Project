from datetime import datetime, timedelta
import random
from locust import HttpUser, task, between

import warnings
warnings.filterwarnings("ignore")
class GachaMicroserviceTasks(HttpUser):
    """Tasks for Gacha microservice endpoints."""
    wait_time = between(1, 2)

    def on_start(self):
        random_number = random.randint(1, 9999999)
        user_code = f"{random_number:07}"

        self.rarities = ["Common", "Rare", "Epic", "Legendary"]
        self.items = {}
        self.gachas = {}
        self.requests_done = 0
        self.user_id = None
        response = self.client.post("/api/player/register",json={"username": f"user{user_code}", "password": "password1", "profilePicture" : "random"}, verify=False)
        if response.status_code == 200:
            self.user_id = response.json()["userId"]
            print(f"User registered successfully. id {self.user_id}")
        else:
            print(f"Failed to register user: {response.status_code}, {response.text}")
        response = self.client.post("/api/player/login",json={"username": f"user{user_code}", "password": "password1"}, verify=False)
        if response.status_code == 200:
            self.token = response.json().get("Access token")
            headers = {"Authorization": f"Bearer {self.token}"}
            print("Access token obtained successfully.")
            res = self.client.put(f"/api/player/increase/{self.user_id}",json={"amount" : 40000000}, headers=headers ,verify=False)
            print(f"increase request status {res.status_code}, {res.text}")
        else:
            self.token = None
            print(f"Failed to obtain token: {response.status_code}, {response.text}")

    @task
    def get_player_collection(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}      
            self.client.get(f"/api/player/gacha/player-collection", headers=headers, verify=False)

    @task
    def get_collection_item_details(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            res = self.client.get(f"/api/player/gacha/player-collection", headers=headers, verify=False)
            if res.status_code == 200:
                collection = res.json()
                if len(collection) > 0:
                    self.client.get(f"/api/player/gacha/player-collection/item/{collection[random.randint(0, len(collection)-1)]["id"]}", headers=headers, verify=False)

    @task
    def get_gacha_details(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            res = self.client.get(f"/api/player/gacha/player-collection", headers=headers, verify=False)
            if res.status_code == 200:
                collection = res.json()
                if len(collection) > 0:
                    self.client.get(f"/api/player/gacha/player-collection/gacha/{collection[random.randint(0, len(collection)-1)]["gachaId"]}", headers=headers, verify=False)

    @task
    def get_system_gacha_collection(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get("/api/player/gacha/system-collection", headers=headers, verify=False)

    @task
    def get_system_gacha_details(self):
        if self.token:
            gacha_id = 1  # Fiksni ID
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get(f"/api/player/gacha/system-collection/{gacha_id}", headers=headers, verify=False)

    @task
    def roll_gacha_legendary(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            for i in range(4):
                response = self.client.post("/api/player/gacha/roll", headers=headers, verify=False, json={"rarity_level": self.rarities[i-1]})
                # if response.status_code != 200: break
                # self.requests_done += 1
                # item = response.json()
                # if item['name'] not in self.gachas:
                #     self.gachas[item['name']] = { "rarity" : item["rarityPercent"] }
                # if item['name'] in self.items:
                #     self.items[item['name']] += 1
                # else:
                #     self.items[item['name']] = 1

    # def on_stop(self):
    #     if self.token:
    #         for gacha in self.gachas:
    #             print(f"{gacha}: {self.gachas[gacha]}")
    #         print(f"\nCalls:{self.requests_done}\n")
    #         for item in self.items:
    #             print(f"{item}: {self.items[item]} approx prob => {(float(self.items[item])/float(self.requests_done))*100.0}")
