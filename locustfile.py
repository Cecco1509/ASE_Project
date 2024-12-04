from locust import HttpUser, TaskSet, task, between

class GachaMicroserviceTasks(TaskSet):
    """Tasks for Gacha microservice endpoints."""
    wait_time = between(1, 2)
    def on_start(self):
    # You can also do it only the first time using «if self.token:»
        response = self.client.post("/api/player/login",json={"username": "user123", "password": "password1"})
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
            self.client.get(f"/api/player/gacha/player-collection/{user_id}", headers=headers)

    @task
    def get_collection_item_details(self):
        if self.token:
            collection_id = 1  # Fiksni ID
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get(f"/api/player/gacha/player-collection/item/{collection_id}", headers=headers)

    @task
    def get_gacha_details(self):
        if self.token:
            user_id = 1  # Fiksni ID
            gacha_id = 1  # Fiksni ID
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get(f"/api/player/gacha/player-collection/{user_id}/gacha/{gacha_id}", headers=headers)

    @task
    def get_system_gacha_collection(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get("/api/player/gacha/system-collection", headers=headers)

    @task
    def get_system_gacha_details(self):
        if self.token:
            gacha_id = 1  # Fiksni ID
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get(f"/api/player/gacha/system-collection/{gacha_id}", headers=headers)

    @task
    def roll_gacha(self):
        if self.token:
            payload = {"gacha_type": "premium", "rank": 1} 
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.post("/api/player/gacha/roll", json=payload, headers=headers)


class PaymentsMicroserviceTasks(TaskSet):
    """Tasks for Payments microservice endpoints."""
    wait_time = between(1, 2)
    def on_start(self):
    # You can also do it only the first time using «if self.token:»
        response = self.client.post("/api/player/login",json={"username": "user123", "password": "password1"})
        if response.status_code == 200:
            self.token = response.json().get("Access token")
            print("Access token obtained successfully.")
        else:
            self.token = None
            print(f"Failed to obtain token: {response.status_code}, {response.text}")


    @task
    def get_transaction_history(self):
        if self.token:
            user_id = 1  # Fiksni ID
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get(f"/api/player/currency{user_id}", headers=headers)

    @task
    def purchase_currency(self):
        if self.token:
            payload = {"amount": 100, "currency": "USD", "rank": 1}  # Rank je fiksno 1
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.post("/api/player/currency/", json=payload, headers=headers)

    @task
    def decrease_currency(self):
        if self.token:
            user_id = 1  # Fiksni ID
            payload = {"amount": 50}
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.put(f"/api/player/decrease/{user_id}", json=payload, headers=headers)

    @task
    def increase_currency(self):
        if self.token:
            user_id = 1  # Fiksni ID
            payload = {"amount": 50}
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.put(f"/api/player/increase/{user_id}", json=payload, headers=headers)


class UsersMicroserviceTasks(TaskSet):
    """Tasks for Users microservice endpoints."""
    wait_time = between(1, 2)
    def on_start(self):
    # You can also do it only the first time using «if self.token:»
        response = self.client.post("/api/player/login",json={"username": "user123", "password": "password1"})
        if response.status_code == 200:
            self.token = response.json().get("Access token")
            print("Access token obtained successfully.")
        else:
            self.token = None
            print(f"Failed to obtain token: {response.status_code}, {response.text}")


    @task
    def get_player_profile(self):
        if self.token:
            user_id = 1  # Fiksni ID
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get(f"/api/player/profile/{user_id}", headers=headers)

    @task
    def update_player_profile(self):
        if self.token:
            user_id = 1  # Fiksni ID
            payload = {"name": "User 1"}
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.put(f"/api/player/update/{user_id}", json=payload, headers=headers)

    @task
    def delete_player(self):
        if self.token:
            user_id = 1  # Fiksni ID
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.delete(f"/api/player/delete/{user_id}", headers=headers)

    @task
    def register_user(self):
        payload = {"username": "user_1", "password": "password123", "rank": 1}  # Rank je fiksno 1
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/api/player/register", json=payload, headers=headers)

    @task
    def login_user(self):
        payload = {"username": "user_1", "password": "password123"}
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/api/player/login", json=payload, headers=headers)

    @task
    def logout_user(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.post("/api/player/logout", headers=headers)


class PlayerAppUser(HttpUser):
    tasks = [GachaMicroserviceTasks, PaymentsMicroserviceTasks, UsersMicroserviceTasks]
    wait_time = between(1, 5)  # Simulacija pauze između zahteva