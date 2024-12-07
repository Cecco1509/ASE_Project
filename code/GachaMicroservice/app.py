import requests
from flask import Flask, request, make_response, jsonify
from python_json_config import ConfigBuilder
import random
from handle_errors import handle_errors
from auth_utils import validate_player_token, validate_admin_token

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
DB_MANAGER_GACHA_URL = config.dbmanagers.gacha
DB_MANAGER_USER_URL = config.dbmanagers.user
AUTH_MICROSERVICE_URL = config.services.authmicroservice
ROLL_PRICE = config.roll.price
ROLL_PROBABILITY = config.roll.probability


""" ----------------- ADMIN ENDPOINTS ----------------- """

@app.route('/api/admin/gacha', methods=['GET'])
@handle_errors
@validate_admin_token
def get_all_gacha():
    """Fetch all gacha items."""
    response = requests.get(DB_MANAGER_GACHA_URL + f'/gacha', verify=False, timeout=config.timeout.medium)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)
        

@app.route('/api/admin/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
@validate_admin_token
def get_single_gacha(gachaId):
    """Fetch a single gacha item by ID."""
    response = requests.get(DB_MANAGER_GACHA_URL + f'/gacha/{gachaId}', verify=False, timeout=config.timeout.medium)
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
    response = requests.post(DB_MANAGER_GACHA_URL + f'/gacha', json=json_data, verify=False, timeout=config.timeout.medium)
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
    response = requests.put(DB_MANAGER_GACHA_URL + f'/gacha/{gachaId}', json=json_data, verify=False, timeout=config.timeout.medium)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

@app.route('/api/admin/gacha/<int:gachaId>', methods=['DELETE'])
@handle_errors
@validate_admin_token
def delete_gacha(gachaId):
    """Delete a gacha item."""
    response = requests.delete(DB_MANAGER_GACHA_URL + f'/gacha/{gachaId}', verify=False, timeout=config.timeout.medium)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

@app.route('/api/admin/gachacollection', methods=['GET'])
@handle_errors
@validate_admin_token
def get_all_gachacollections():
    """Fetch all gacha collections."""
    response = requests.get(DB_MANAGER_GACHA_URL + f'/gachacollection', verify=False, timeout=config.timeout.medium)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

""" ----------------- PLAYER ENDPOINTS ----------------- """

"""Player Collection Endpoints"""

# Get player's gacha collection.
@app.route('/api/player/gacha/player-collection', methods=['GET'])
@handle_errors
@validate_player_token
def get_gacha_collection(auth_response=None):
    userId = auth_response.json()['userId']
    response = requests.get(f'{DB_MANAGER_GACHA_URL}/gachacollection/{userId}', verify=False, timeout=config.timeout.medium)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get player's gacha collection item
@app.route('/api/player/gacha/player-collection/item/<int:collectionId>', methods=['GET'])
@handle_errors
def get_gacha_collection_details(collectionId):
    response = requests.get(f'{DB_MANAGER_GACHA_URL}/gachacollection/item/{collectionId}', verify=False, timeout=config.timeout.medium)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get player's gacha item details
@app.route('/api/player/gacha/player-collection/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
@validate_player_token
def get_gacha_details(gachaId, auth_response=None):
    userId = auth_response.json()['userId']
    user_gacha_collection_response = requests.get(f'{DB_MANAGER_GACHA_URL}/gachacollection/{userId}', verify=False, timeout=config.timeout.medium)
    user_gacha_collection_response.raise_for_status()
    user_gacha_collection = user_gacha_collection_response.json()

    # check if the gacha item is in the player's collection
    if not any(item['gachaId'] == gachaId for item in user_gacha_collection):
        return make_response(jsonify({"message":"Gacha item not found in player's collection"}), 404)
    
    # the gacha item is in the player's collection, get the details
    gacha_item_response = requests.get(f'{DB_MANAGER_GACHA_URL}/gacha/{gachaId}', verify=False, timeout=config.timeout.medium)
    gacha_item_response.raise_for_status()
    gacha_item = gacha_item_response.json()

    return make_response(gacha_item, gacha_item_response.status_code)

"""System Collection Endpoints"""

# Get full system gacha collection.
@app.route('/api/player/gacha/system-collection', methods=['GET'])
@handle_errors
@validate_player_token
def get_system_gacha_collection(auth_response=None):
    response = requests.get(f'{DB_MANAGER_GACHA_URL}/gacha', verify=False, timeout=config.timeout.medium)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get details of a specific system gacha item.
@app.route('/api/player/gacha/system-collection/<int:gachaId>', methods=['GET'])
@handle_errors
@validate_player_token
def get_system_gacha_details(gachaId, auth_response=None):
    response = requests.get(f'{DB_MANAGER_GACHA_URL}/gacha/{gachaId}', verify=False, timeout=config.timeout.medium)
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

"""Gacha Roll Endpoints"""

# Roll a gacha
@app.route('/api/player/gacha/roll', methods=['POST'])
@handle_errors
@validate_player_token
def roll_gacha(auth_response=None):
    # Check if the request contains JSON data
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)

    # Validate the JSON data
    is_valid, validation_message = is_valid_roll_data(json_data)
    if not is_valid:
        return make_response(jsonify({"message": validation_message}), 400)
    rarity_level = json_data["rarity_level"]

    # Fetch user info to verify in-game currency
    userId = auth_response.json()['userId']
    user_response = requests.get(f'{DB_MANAGER_USER_URL}/user/{userId}', headers=request.headers, verify=False, timeout=config.timeout.medium)
    print("user_response", user_response,flush=True)
    if user_response.status_code == 404:
        return make_response(jsonify({"message": "User not found"}), 404)
    elif user_response.status_code != 200:
        return make_response(jsonify({"message": "Error retrieving user info"}), 500)

    # Check the user's status and make sure they are active
    user = user_response.json()
    if user['status'] != 'ACTIVE':
        return make_response(jsonify({"message":"User is not active"}), 403)

    # Get the user's in-game currency
    userIngameCurrency = user['ingameCurrency']
    userId = user['id']

    # Check if the user has enough ingame currency to roll
    roll_price = getattr(ROLL_PRICE,rarity_level)
    if userIngameCurrency < roll_price:
        return make_response(jsonify({"message":"Insufficient in-game currency"}), 400)
    
    # Fetch all gacha items
    gacha_response = requests.get(DB_MANAGER_GACHA_URL + f'/gacha', verify=False, timeout=config.timeout.medium)
    if gacha_response.status_code != 200:
        return make_response(jsonify({"message": "Error retrieving gacha items"}), 500)
    gacha_items = gacha_response.json()

    # Randomly select a gacha item
    selected_gacha = select_gacha(gacha_items, rarity_level)

    # Deduct the roll cost from the user's in-game currency
    userIngameCurrency -= roll_price
    update_user_response = requests.patch(
        f'{DB_MANAGER_USER_URL}/user/{userId}', 
        json={"ingameCurrency":userIngameCurrency},
        verify=False,
        timeout=config.timeout.medium
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
        verify=False,
        timeout=config.timeout.medium
    )
    create_gacha_collection_response.raise_for_status()

    # TODO: handle failures, rollback changes if necessary

    if create_gacha_collection_response.status_code != 200:
        return make_response(jsonify({"message": "Error adding gacha item to player's collection"}), 500)

    return make_response(selected_gacha, 200)

def select_gacha(gacha_items, roll_type):
    """
    Select a gacha item based on rarity distribution with different probability adjustments
    for each roll type (Common, Rare, Epic, Legendary).
    """
    
    # Define rarity thresholds for categorizing items based on their rarityPercent
    rarity_groups = {
        "Common": lambda x: x >= 5,          # Common items have rarity >= 5
        "Uncommon": lambda x: 1.5 <= x < 5,  # Uncommon items have rarity between 1.5 and 5
        "Rare": lambda x: 0.5 <= x < 1.5,    # Rare items have rarity between 0.5 and 1.5
        "Legendary": lambda x: x < 0.5       # Legendary items have rarity < 0.5
    }

    # Bias weights for each roll type: This dictates how likely each rarity group is to be selected
    bias_table = {
        "Common": {"Common": 50, "Uncommon": 30, "Rare": 15, "Legendary": 5}, # Common roll prefers common items
        "Rare": {"Common": 25, "Uncommon": 35, "Rare": 30, "Legendary": 10}, # Rare roll gives more weight to rare items
        "Epic": {"Common": 10, "Uncommon": 20, "Rare": 40, "Legendary": 30}, # Epic roll favors rare and legendary items
        "Legendary": {"Common": 5, "Uncommon": 10, "Rare": 30, "Legendary": 55} # Legendary roll heavily favors legendary items
    }

    # Validate roll type
    if roll_type not in bias_table:
        # PS: this will never happen because we validate the data before calling this function
        roll_type = "Common"

    # Initialize an empty list to store the weighted items
    weighted_items = []

    if roll_type == "Common":
        # For "Common" roll type, we use the original rarityPercent and normalize it
        # The selection is purely based on the item rarity, without any dynamic adjustment
        total_rarity = sum(item["rarityPercent"] for item in gacha_items)
        for item in gacha_items:
            # Normalize the rarityPercent to ensure total probabilities sum to 100
            item["normalizedPercent"] = item["rarityPercent"] / total_rarity * 100
            weighted_items.append((item, item["normalizedPercent"]))
    else:
        # For other roll types, adjust the weights based on rarity group and bias table
        for item in gacha_items:
            # Find which rarity group the item belongs to based on its rarityPercent
            group = next((k for k, condition in rarity_groups.items() if condition(item["rarityPercent"])), None)
            if group:
                # Apply bias based on the group and the selected roll type
                adjusted_weight = item["rarityPercent"] * bias_table[roll_type][group]
                weighted_items.append((item, adjusted_weight))

    # Normalize the total weights to ensure the probabilities sum to 1 (100%)
    total_weight = sum(weight for _, weight in weighted_items)
    normalized_weights = [weight / total_weight for _, weight in weighted_items]

    print(f"Normalized weights: {normalized_weights}")

    # Perform the selection based on the normalized probabilities
    selected_item = random.choices(
        population=[item for item, _ in weighted_items],
        weights=normalized_weights,
        k=1  # Only one selection
    )[0]

    # Remove the "normalizedPercent" field before returning the selected item
    selected_item.pop("normalizedPercent", None)

    return selected_item

def is_valid_roll_data(data):
    required_fields = {
        "rarity_level": str
    }

    for field, expected_type in required_fields.items():
        if field not in data:
            return False, f"Missing required field: {field}"
        if not isinstance(data[field], expected_type):
            return False, f"Invalid type for field '{field}': Expected {expected_type.__name__}"
    
    # Additional validation: rarity_level should be either: "Common", "Rare", "Epic", "Legendary"
    if data["rarity_level"] not in ["Common", "Rare", "Epic", "Legendary"]:
        return False, "Invalid rarity level. Must be one of: Common, Rare, Epic, Legendary"

    return True, "Data is valid"

def create_app():
    return app