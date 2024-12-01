import requests
from flask import Flask, request, make_response, jsonify
from python_json_config import ConfigBuilder
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
    response = requests.get(DB_MANAGER_GACHA_URL + f'/gacha')
    response.raise_for_status()
    gacha_items = response.json()
    return make_response(jsonify(gacha_items), response.status_code)
        

@app.route('/api/admin/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
@validate_admin_token
def get_single_gacha(gachaId):
    """Fetch a single gacha item by ID."""
    response = requests.get(DB_MANAGER_GACHA_URL + f'/gacha/{gachaId}')
    response.raise_for_status()
    return make_response(jsonify(response.json()), response.status_code)

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
    response = requests.post(DB_MANAGER_GACHA_URL + f'/gacha', json=json_data)
    response.raise_for_status()
    return make_response(jsonify(response.json()), response.status_code)

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
    response = requests.put(DB_MANAGER_GACHA_URL + f'/gacha/{gachaId}', json=json_data)
    response.raise_for_status()
    return make_response(jsonify(response.json()), 200)

@app.route('/api/admin/gacha/<int:gachaId>', methods=['DELETE'])
@handle_errors
@validate_admin_token
def delete_gacha(gachaId):
    """Delete a gacha item."""
    response = requests.delete(DB_MANAGER_GACHA_URL + f'/gacha/{gachaId}')
    response.raise_for_status()
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/admin/gachacollection', methods=['GET'])
@handle_errors
@validate_admin_token
def get_all_gachacollections():
    """Fetch all gacha collections."""
    response = requests.get(DB_MANAGER_GACHA_URL + f'/gachacollection')
    response.raise_for_status()
    gacha_collections = response.json()
    return make_response(jsonify(gacha_collections), response.status_code)

""" ----------------- PLAYER ENDPOINTS ----------------- """

"""Player Collection Endpoints"""

# Get player's gacha collection.
@app.route('/api/player/gacha/player-collection/<int:userId>', methods=['GET'])
@handle_errors
@validate_player_token
def get_gacha_collection(userId, auth_response=None):
    print("Auth response:", auth_response.json(), flush=True)

    response = requests.get(f'{DB_MANAGER_GACHA_URL}/gachacollection/{userId}')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get player's gacha collection item
@app.route('/api/player/gacha/player-collection/item/<int:collectionId>', methods=['GET'])
@handle_errors
def get_gacha_collection_details(collectionId):
    response = requests.get(f'{DB_MANAGER_GACHA_URL}/gachacollection/item/{collectionId}')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get player's gacha item details
@app.route('/api/player/gacha/player-collection/<int:userId>/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
@validate_player_token
def get_gacha_details(userId, gachaId, auth_response=None):
    user_gacha_collection_response = requests.get(f'{DB_MANAGER_GACHA_URL}/gachacollection/{userId}')
    user_gacha_collection_response.raise_for_status()
    user_gacha_collection = user_gacha_collection_response.json()

    # check if the gacha item is in the player's collection
    if not any(item['gachaId'] == gachaId for item in user_gacha_collection):
        return make_response(jsonify({"message":"Gacha item not found in player's collection"}), 404)
    
    # the gacha item is in the player's collection, get the details
    gacha_item_response = requests.get(f'{DB_MANAGER_GACHA_URL}/gacha/{gachaId}')
    gacha_item_response.raise_for_status()
    gacha_item = gacha_item_response.json()

    return make_response(gacha_item, 200)

"""System Collection Endpoints"""

# Get full system gacha collection.
@app.route('/api/player/gacha/system-collection', methods=['GET'])
@handle_errors
@validate_player_token
def get_system_gacha_collection(auth_response=None):
    response = requests.get(f'{DB_MANAGER_GACHA_URL}/gacha')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get details of a specific system gacha item.
@app.route('/api/player/gacha/system-collection/<int:gachaId>', methods=['GET'])
@handle_errors
@validate_player_token
def get_system_gacha_details(gachaId, auth_response=None):
    response = requests.get(f'{DB_MANAGER_GACHA_URL}/gacha/{gachaId}')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

"""Gacha Roll Endpoints"""

# Roll a gacha
@app.route('/api/player/gacha/roll', methods=['POST'])
@handle_errors
@validate_player_token
def roll_gacha(auth_response=None):
    print("Rolling gacha", flush=True)
    json_data = request.get_json()
    print(json_data, flush=True)

    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)
    
    is_valid, validation_message = is_valid_roll_data(json_data)
    if not is_valid:
        return make_response(jsonify({"message": validation_message}), 400)
    
    userId = json_data['userId']
    get_user_response = requests.get(f'{DB_MANAGER_USER_URL}/user/{userId}')

    get_user_response.raise_for_status()

    print("Got user", flush=True)
    print(get_user_response.json(), flush=True)
    
    user = get_user_response.json()
    userIngameCurrency = user['ingameCurrency']

    # check if the user has enough ingame currency to roll
    if userIngameCurrency < ROLL_PRICE:
        return make_response(jsonify({"message":"Insufficient in-game currency"}), 400)
    
    # get a random gacha from the system collection
    get_random_gacha_response = requests.get(f'{DB_MANAGER_GACHA_URL}/gacha/random')
    get_random_gacha_response.raise_for_status()
    random_gacha = get_random_gacha_response.json()

    # deduct the roll price from the user's in-game currency
    userIngameCurrency -= ROLL_PRICE
    update_user_response = requests.patch(
        f'{DB_MANAGER_USER_URL}/user/{userId}', 
        json={"ingameCurrency":userIngameCurrency}
    )
    update_user_response.raise_for_status()

    # add the gacha to the player's collection
    create_gacha_collection_response = requests.post(
        f'{DB_MANAGER_GACHA_URL}/gachacollection', 
        json={
            "gachaId":random_gacha['id'],
            "userId":userId,
            "source":"ROLL"
        }
    )
    create_gacha_collection_response.raise_for_status()

    # TODO: handle failures, rollback changes if necessary

    return make_response(create_gacha_collection_response.json(), create_gacha_collection_response.status_code)

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