from locust import HttpUser, TaskSet, task, between


class GachaMicroserviceTasks(TaskSet):
    """Tasks for Gacha microservice endpoints."""
    wait_time = between(1, 2)
    def on_start(self):
        # Step 1: Register a new user (if needed)
        registration_response = self.client.post("/api/player/register", json={
            "username": "test_user", 
            "password": "test_password"
        })
        
        if registration_response.status_code == 200:
            print("User registered successfully.")
        else:
            print(f"Failed to register user: {registration_response.status_code}, {registration_response.text}")
        
        # Step 2: Login to obtain token
        login_response = self.client.post("/login", json={
            "username": "test_user", 
            "password": "test_password"
        })
        
        if login_response.status_code == 200:
            self.token = login_response.json().get("access_token")
            print("Access token obtained successfully.")
        else:
            self.token = None
            print(f"Failed to obtain token: {login_response.status_code}, {login_response.text}")


    @task
    def get_player_collection(self):
        if self.token:
            user_id = 1  # Fiksni ID
            self.client.get(f"/api/player/gacha/player-collection/{user_id}")

    @task
    def get_collection_item_details(self):
        if self.token:
            collection_id = 1  # Fiksni ID
            self.client.get(f"/api/player/gacha/player-collection/item/{collection_id}")

    @task
    def get_gacha_details(self):
        if self.token:
            user_id = 1  # Fiksni ID
            gacha_id = 1  # Fiksni ID
            self.client.get(f"/api/player/gacha/player-collection/{user_id}/gacha/{gacha_id}")

    @task
    def get_system_gacha_collection(self):
        if self.token:
            self.client.get("/api/player/gacha/system-collection")

    @task
    def get_system_gacha_details(self):
        if self.token:
            gacha_id = 1  # Fiksni ID
            self.client.get(f"/api/player/gacha/system-collection/{gacha_id}")

    @task
    def roll_gacha(self):
        if self.token:
            payload = {"gacha_type": "premium", "rank": 1}  # Rank je fiksno 1
            self.client.post("/api/player/gacha/roll", json=payload)


class PaymentsMicroserviceTasks(TaskSet):
    """Tasks for Payments microservice endpoints."""
    wait_time = between(1, 2)
    def on_start(self):
        # Step 1: Register a new user (if needed)
        registration_response = self.client.post("/api/player/register", json={
            "username": "test_user", 
            "password": "test_password"
        })
        
        if registration_response.status_code == 200:
            print("User registered successfully.")
        else:
            print(f"Failed to register user: {registration_response.status_code}, {registration_response.text}")
        
        # Step 2: Login to obtain token
        login_response = self.client.post("/login", json={
            "username": "test_user", 
            "password": "test_password"
        })
        
        if login_response.status_code == 200:
            self.token = login_response.json().get("access_token")
            print("Access token obtained successfully.")
        else:
            self.token = None
            print(f"Failed to obtain token: {login_response.status_code}, {login_response.text}")


    @task
    def get_transaction_history(self):
        if self.token:
            user_id = 1  # Fiksni ID
            self.client.get(f"/api/player/currency{user_id}")

    @task
    def purchase_currency(self):
        if self.token:
            payload = {"amount": 100, "currency": "USD", "rank": 1}  # Rank je fiksno 1
            self.client.post("/api/player/currency/", json=payload)

    @task
    def decrease_currency(self):
        if self.token:
            user_id = 1  # Fiksni ID
            payload = {"amount": 50}
            self.client.put(f"/api/player/decrease/{user_id}", json=payload)

    @task
    def increase_currency(self):
        if self.token:
            user_id = 1  # Fiksni ID
            payload = {"amount": 50}
            self.client.put(f"/api/player/increase/{user_id}", json=payload)


class UsersMicroserviceTasks(TaskSet):
    """Tasks for Users microservice endpoints."""
    wait_time = between(1, 2)
    def on_start(self):
        # Step 1: Register a new user (if needed)
        registration_response = self.client.post("/api/player/register", json={
            "username": "test_user", 
            "password": "test_password"
        })
        
        if registration_response.status_code == 200:
            print("User registered successfully.")
        else:
            print(f"Failed to register user: {registration_response.status_code}, {registration_response.text}")
        
        # Step 2: Login to obtain token
        login_response = self.client.post("/login", json={
            "username": "test_user", 
            "password": "test_password"
        })
        
        if login_response.status_code == 200:
            self.token = login_response.json().get("access_token")
            print("Access token obtained successfully.")
        else:
            self.token = None
            print(f"Failed to obtain token: {login_response.status_code}, {login_response.text}")


    @task
    def get_player_profile(self):
        if self.token:
            user_id = 1  # Fiksni ID
            self.client.get(f"/api/player/profile/{user_id}")

    @task
    def update_player_profile(self):
        if self.token:
            user_id = 1  # Fiksni ID
            payload = {"name": "User 1"}
            self.client.put(f"/api/player/update/{user_id}", json=payload)

    @task
    def delete_player(self):
        if self.token:
            user_id = 1  # Fiksni ID
            self.client.delete(f"/api/player/delete/{user_id}")

    @task
    def register_user(self):
        payload = {"username": "user_1", "password": "password123", "rank": 1}  # Rank je fiksno 1
        self.client.post("/api/player/register", json=payload)

    @task
    def login_user(self):
        payload = {"username": "user_1", "password": "password123"}
        self.client.post("/api/player/login", json=payload)

    @task
    def logout_user(self):
        if self.token:
            self.client.post("/api/player/logout")


class PlayerAppUser(HttpUser):
    tasks = [GachaMicroserviceTasks, PaymentsMicroserviceTasks, UsersMicroserviceTasks]
    wait_time = between(1, 5)  # Simulacija pauze između zahteva
