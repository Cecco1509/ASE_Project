import requests, time

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

app = Flask(__name__, instance_relative_config=True)

class StatusEnum(Enum):
    ACTIVE = "active"
    INACTIVE = "unknown"
    BANNED = "banned"

@app.route('/api/admin/users', methods=['GET'])
def get_players():
    try:
        response = requests.get(DATABASE_API_URL)
        if response.status_code == 200:
            players_data = response.json()
            players = []
            for player_data in players_data:
                player = {
                    "id": player_data["id"],
                    "ingameCurrency": player_data["ingameCurrency"],
                    "profile_pic": player_data["profile_pic"],
                    "registration_date": player_data["registration_date"],
                    "status": StatusEnum(player_data["status"]).value
                }
                players.append(player)

            return make_response(jsonify(players), 200)
        else:
            return make_response(jsonify({"error": "Failed to fetch player data from the database API."}), 500)

    except requests.RequestException as e:
        return make_response(jsonify({"error": f"An error occurred while fetching data: {str(e)}"}), 500)

@app.route('/api/admin/users/<int:user_id>', methods=['GET'])
def get_player(user_id):
    try:
        response = requests.get(f"{DATABASE_API_URL}/{user_id}")
        
        if response.status_code == 200:
            player_data = response.json()

            player = {
                "id": player_data["id"],
                "ingameCurrency": player_data["ingameCurrency"],
                "profile_pic": player_data["profile_pic"],
                "registration_date": player_data["registration_date"],
                "status": StatusEnum(player_data["status"]).value 
            }

            return make_response(jsonify(player), 200)
        else:
            return make_response(jsonify({"error": f"Player with ID {user_id} not found."}), 404)

    except requests.RequestException as e:
        return make_response(jsonify({"error": f"An error occurred while fetching data: {str(e)}"}), 500)
    
@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
def update_player(user_id):
    try:
        player_data = request.get_json()
        if not player_data:
            return make_response(jsonify({"error": "No data provided"}), 400)
        
        updated_data = {
            "id": user_id,  
            "ingameCurrency": player_data.get("ingameCurrency"),
            "profile_pic": player_data.get("profile_pic"),
            "registration_date": player_data.get("registration_date"),
            "status": player_data.get("status") if player_data.get("status") in StatusEnum.__members__ else "inactive"
        }

        response = requests.put(f"{DATABASE_API_URL}/{user_id}", json=updated_data)
        if response.status_code == 200:
            return make_response(jsonify({"message": "Player updated successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Failed to update player data"}), response.status_code)

    except requests.RequestException as e:
        return make_response(jsonify({"error": f"An error occurred while updating data: {str(e)}"}), 500)

@app.route('/api/admin/users/ban/<int:user_id>', methods=['POST'])
def ban_player(user_id):
    try:
        updated_data = {
            "status": StatusEnum.BANNED.value 
        }

        response = requests.put(f"{DATABASE_API_URL}/{user_id}", json=updated_data)

        if response.status_code == 200:
            return make_response(jsonify({"message": f"Player {user_id} has been banned successfully."}), 200)
        elif response.status_code == 404:
            return make_response(jsonify({"error": f"Player with ID {user_id} not found."}), 404)
        else:
            return make_response(jsonify({"error": "Failed to ban player. Please try again later."}), response.status_code)
    except requests.RequestException as e:
        return make_response(jsonify({"error": f"An error occurred while banning the player: {str(e)}"}), 500)

def create_app():
    return app