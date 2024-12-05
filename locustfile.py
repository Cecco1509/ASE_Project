from locust import HttpUser, task, between

class GachaMicroserviceTasks(HttpUser):
    """Tasks for Gacha microservice endpoints."""
    wait_time = between(1, 2)
    def on_start(self):
    # You can also do it only the first time using «if self.token:»
        response = self.client.post("/api/player/login",json={"username": "user123", "password": "password1"}, verify=False)
        if response.status_code == 200:
            self.token = response.json().get("Access token")
            print("Access token obtained successfully.")
        else:
            self.token = None
            print(f"Failed to obtain token: {response.status_code}, {response.text}")


    @task
    def get_player_collection(self):
        if self.token:
            user_id = 1  # Fiksni ID
            headers = {"Authorization": f"Bearer {self.token}"}      
            self.client.get(f"/api/player/gacha/player-collection/{user_id}", headers=headers, verify=False)

    @task
    def get_collection_item_details(self):
        if self.token:
            collection_id = 1  # Fiksni ID
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get(f"/api/player/gacha/player-collection/item/{collection_id}", headers=headers, verify=False)

    @task
    def get_gacha_details(self):
        if self.token:
            user_id = 1  # Fiksni ID
            gacha_id = 1  # Fiksni ID
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get(f"/api/player/gacha/player-collection/{user_id}/gacha/{gacha_id}", headers=headers, verify=False)

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
    def roll_gacha(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.post("/api/player/gacha/roll", headers=headers, verify=False)


