import requests
from flask import Flask, request, make_response, jsonify
from python_json_config import ConfigBuilder
import random
from handle_errors import handle_errors
from auth_utils import validate_player_token, validate_admin_token

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
DB_MANAGER_GACHA_URL = config.dbmanagers.gacha
DB_MANAGER_USER_URL = config.dbmanagers.user
ROLL_PRICE = config.system_settings.gacha_roll_price


""" ----------------- ADMIN ENDPOINTS ----------------- """

@app.route('/api/admin/gacha', methods=['GET'])
@handle_errors
@validate_admin_token
def get_all_gacha():
    """Fetch all gacha items."""
    response = requests.get(DB_MANAGER_GACHA_URL + f'/gacha', verify=False)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)
        

@app.route('/api/admin/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
@validate_admin_token
def get_single_gacha(gachaId):
    """Fetch a single gacha item by ID."""
    response = requests.get(DB_MANAGER_GACHA_URL + f'/gacha/{gachaId}', verify=False)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

@app.route('/api/admin/gacha', methods=['POST'])
@handle_errors
@validate_admin_token
def create_gacha():
    """Create a new gacha item."""
    json_data = request.get_json()

    # check if data is valid
    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)
    
    is_valid, validation_message = is_valid_gacha_data(json_data)
    if not is_valid:
        return make_response(jsonify({"message": validation_message}), 400)

    # all data is valid, send to the DB manager
    response = requests.post(DB_MANAGER_GACHA_URL + f'/gacha', json=json_data, verify=False)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

def is_valid_gacha_data(data):
    """
    Validate the input JSON data for creating a gacha item.
    Checks for required fields, data types, and formats.
    """
    required_fields = {
        "name": str,
        "image": str,
        "rarityPercent": float,
        "description": str,
    }

    for field, expected_type in required_fields.items():
        if field not in data:
            return False, f"Missing required field: {field}"
        if not isinstance(data[field], expected_type):
            return False, f"Invalid type for field '{field}': Expected {expected_type.__name__}"

    # Additional validation: rarityPercent should be between 0 and 100
    if not (0 <= data["rarityPercent"] <= 100):
        return False, "Rarity percent must be a value between 0 and 1."

    return True, "Data is valid"

# TODO: use patch instead of put, so we can only update the fields that are provided
@app.route('/api/admin/gacha/<int:gachaId>', methods=['PUT'])
@handle_errors
@validate_admin_token
def update_gacha(gachaId):
    """Update a gacha item."""
    json_data = request.get_json()

    # check if data is valid
    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)
    
    is_valid, validation_message = is_valid_gacha_data(json_data)
    if not is_valid:
        return make_response(jsonify({"message": validation_message}), 400)

    # all data is valid, send to the DB manager
    response = requests.put(DB_MANAGER_GACHA_URL + f'/gacha/{gachaId}', json=json_data, verify=False)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

@app.route('/api/admin/gacha/<int:gachaId>', methods=['DELETE'])
@handle_errors
@validate_admin_token
def delete_gacha(gachaId):
    """Delete a gacha item."""
    response = requests.delete(DB_MANAGER_GACHA_URL + f'/gacha/{gachaId}', verify=False)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

@app.route('/api/admin/gachacollection', methods=['GET'])
@handle_errors
@validate_admin_token
def get_all_gachacollections():
    """Fetch all gacha collections."""
    response = requests.get(DB_MANAGER_GACHA_URL + f'/gachacollection', verify=False)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

""" ----------------- PLAYER ENDPOINTS ----------------- """

"""Player Collection Endpoints"""

# Get player's gacha collection.
@app.route('/api/player/gacha/player-collection/<int:userId>', methods=['GET'])
@handle_errors
@validate_player_token
def get_gacha_collection(userId, auth_response=None):
    print("Auth response:", auth_response.json(), flush=True)

    response = requests.get(f'{DB_MANAGER_GACHA_URL}/gachacollection/{userId}', verify=False)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get player's gacha collection item
@app.route('/api/player/gacha/player-collection/item/<int:collectionId>', methods=['GET'])
@handle_errors
def get_gacha_collection_details(collectionId):
    response = requests.get(f'{DB_MANAGER_GACHA_URL}/gachacollection/item/{collectionId}', verify=False)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get player's gacha item details
@app.route('/api/player/gacha/player-collection/<int:userId>/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
@validate_player_token
def get_gacha_details(userId, gachaId, auth_response=None):
    user_gacha_collection_response = requests.get(f'{DB_MANAGER_GACHA_URL}/gachacollection/{userId}', verify=False)
    user_gacha_collection_response.raise_for_status()
    user_gacha_collection = user_gacha_collection_response.json()

    # check if the gacha item is in the player's collection
    if not any(item['gachaId'] == gachaId for item in user_gacha_collection):
        return make_response(jsonify({"message":"Gacha item not found in player's collection"}), 404)
    
    # the gacha item is in the player's collection, get the details
    gacha_item_response = requests.get(f'{DB_MANAGER_GACHA_URL}/gacha/{gachaId}', verify=False)
    gacha_item_response.raise_for_status()
    gacha_item = gacha_item_response.json()

    return make_response(gacha_item, gacha_item_response.status_code)

"""System Collection Endpoints"""

# Get full system gacha collection.
@app.route('/api/player/gacha/system-collection', methods=['GET'])
@handle_errors
@validate_player_token
def get_system_gacha_collection(auth_response=None):
    response = requests.get(f'{DB_MANAGER_GACHA_URL}/gacha', verify=False)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get details of a specific system gacha item.
@app.route('/api/player/gacha/system-collection/<int:gachaId>', methods=['GET'])
@handle_errors
@validate_player_token
def get_system_gacha_details(gachaId, auth_response=None):
    response = requests.get(f'{DB_MANAGER_GACHA_URL}/gacha/{gachaId}', verify=False)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

"""Gacha Roll Endpoints"""

# Roll a gacha
@app.route('/api/player/gacha/roll', methods=['POST'])
@handle_errors
@validate_player_token
def roll_gacha(auth_response=None):

    # TODO remove this
    print("Auth response:", auth_response.json(), flush=True)
    
    # TODO remove this
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)

    is_valid, validation_message = is_valid_roll_data(json_data)
    if not is_valid:
        return make_response(jsonify({"message": validation_message}), 400)

    

    
    
    
    
    # Fetch user info to verify in-game currency
    userId = json_data['userId']
    user_response = requests.get(f'{DB_MANAGER_USER_URL}/user/{userId}', verify=False)

    # Check if the user exists
    if user_response.status_code == 404:
        return make_response(jsonify({"message": "User not found"}), 404)
    elif user_response.status_code != 200:
        return make_response(jsonify({"message": "Error retrieving user info"}), 500)
    
    # Get the user's in-game currency
    user = user_response.json()
    userIngameCurrency = user['ingameCurrency']

    # Check if the user has enough ingame currency to roll
    if userIngameCurrency < ROLL_PRICE:
        return make_response(jsonify({"message":"Insufficient in-game currency"}), 400)
    
    # Fetch all gacha items
    gacha_response = requests.get(DB_MANAGER_GACHA_URL + f'/gacha', verify=False)
    if gacha_response.status_code != 200:
        return make_response(jsonify({"message": "Error retrieving gacha items"}), 500)
    gacha_items = gacha_response.json()

    # Randomly select a gacha item
    selected_gacha = select_gacha(gacha_items)

    # Deduct the roll cost from the user's in-game currency
    userIngameCurrency -= ROLL_PRICE
    update_user_response = requests.patch(
        f'{DB_MANAGER_USER_URL}/user/{userId}', 
        json={"ingameCurrency":userIngameCurrency}
    )
    if update_user_response.status_code != 200:
        return make_response(jsonify({"message": "Error updating the user's in-game currency balance"}), 500)

    # Add the selected gacha to the player's collection
    create_gacha_collection_response = requests.post(
        f'{DB_MANAGER_GACHA_URL}/gachacollection', 
        json={
            "gachaId":selected_gacha['id'],
            "userId":userId,
            "source":"ROLL"
        },
        verify=False
    )
    create_gacha_collection_response.raise_for_status()

    # TODO: handle failures, rollback changes if necessary

    return make_response(create_gacha_collection_response.json(), create_gacha_collection_response.status_code)

def select_gacha(gacha_items):
    """
    Select a gacha item based on rarity distribution.
    """
    # Create a weighted list where higher rarityPercent means lower chance of selection
    weighted_gacha_list = []
    for gacha in gacha_items:
        # Rarity Distribution: Lower rarityPercent means the item is more common, while higher rarityPercent means the item is rarer.
        weight = 101 - gacha["rarityPercent"]
        weighted_gacha_list.extend([gacha] * weight)

    # Randomly select an item from the weighted list
    return random.choice(weighted_gacha_list)

# TODO: remove this
def is_valid_roll_data(data):
    required_fields = {
        "userId": int
    }

    for field, expected_type in required_fields.items():
        if field not in data:
            return False, f"Missing required field: {field}"
        if not isinstance(data[field], expected_type):
            return False, f"Invalid type for field '{field}': Expected {expected_type.__name__}"

    return True, "Data is valid"

def create_app():
    return app