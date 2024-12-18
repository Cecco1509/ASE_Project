from flask import Flask, request, make_response, jsonify
from python_json_config import ConfigBuilder
from handle_errors import handle_errors
from datetime import datetime
import random
from gacha_mock_db import *

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
ROLL_PRICE = config.roll.price
ROLL_PROBABILITY = config.roll.probability

""" ------------------ ADMIN ENDPOINTS ------------------ """

@app.route('/api/admin/gacha', methods=['GET'])
@handle_errors
def get_all_gacha():
    """Fetch all gacha items."""
    is_valid, message, status_code = mock_validate_token(request)
    if not is_valid:
        return make_response(jsonify({"message": message}), status_code)

    return make_response(jsonify(mock_gacha_list), 200)

"""Fetch a single gacha item by ID."""
@app.route('/api/admin/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
def get_single_gacha(gachaId):
    # cbeck if gachaId is valid
    is_valid, message, status_code = mock_validate_token(request)
    if not is_valid:
        return make_response(jsonify({"message": message}), status_code)

    if gachaId < 1 or gachaId > len(mock_gacha_list):
        return make_response(jsonify({"message": f"Gacha item with ID {gachaId} not found"}), 404)
    return make_response(jsonify(mock_gacha_list[gachaId-1]), 200)

@app.route('/api/admin/gacha', methods=['POST'])
@handle_errors
def create_gacha():
    """Create a new gacha item."""
    is_valid, message, status_code = mock_validate_token(request)
    if not is_valid:
        return make_response(jsonify({"message": message}), status_code)

    json_data = request.get_json()

    # check if data is valid
    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)
    
    is_valid, validation_message = is_valid_gacha_data(json_data)
    if not is_valid:
        return make_response(jsonify({"message": validation_message}), 400)

    # all data is valid, add the new gacha item to the mock list
    new_gacha = {
        'id': len(mock_gacha_list) + 1,
        'name': json_data['name'],
        'description': json_data['description'],
        'image': json_data['image'],
        'rarityPercent': json_data['rarityPercent']
    }
    mock_gacha_list.append(new_gacha)
    return make_response({"gachaId": new_gacha['id']}, 200)

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
        return False, "Rarity percent must be a value between 0 and 100."

    return True, "Data is valid"

@app.route('/api/admin/gacha/<int:gachaId>', methods=['PUT'])
@handle_errors
def update_gacha(gachaId):
    """Update a gacha item."""
    is_valid, message, status_code = mock_validate_token(request)
    if not is_valid:
        return make_response(jsonify({"message": message}), status_code)

    json_data = request.get_json()

    # check if data is valid
    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)
    
    is_valid, validation_message = is_valid_gacha_data(json_data)
    if not is_valid:
        return make_response(jsonify({"message": validation_message}), 400)

    # all data is valid, update the gacha item in the mock list
    gacha_item = next((gacha for gacha in mock_gacha_list if gacha['id'] == gachaId), None)
    if not gacha_item:
        return make_response(jsonify({"message": f"Gacha item with ID {gachaId} not found"}), 404)
    
    gacha_item.update(json_data)
    return make_response({"message":"Gacha sucessfully updated."}, 200)

@app.route('/api/admin/gacha/<int:gachaId>', methods=['DELETE'])
@handle_errors
def delete_gacha(gachaId):
    """Delete a gacha item."""
    is_valid, message, status_code = mock_validate_token(request)
    if not is_valid:
        return make_response(jsonify({"message": message}), status_code)
    global mock_gacha_list

    # check if gachaId is valid
    gacha_item = next((gacha for gacha in mock_gacha_list if gacha['id'] == gachaId), None)
    if not gacha_item:
        return make_response(jsonify({"message": f"Gacha item with ID {gachaId} not found"}), 404)
    
    # all data is valid, delete the gacha item from the mock list
    # mock_gacha_list = [gacha for gacha in mock_gacha_list if gacha['id'] != gachaId]

    return make_response({"message":"Gacha sucessfully deleted."}, 200)

@app.route('/api/admin/gachacollection', methods=['GET'])
@handle_errors
def get_all_gachacollections():
    """Get all gacha collections."""
    is_valid, message, status_code = mock_validate_token(request)
    if not is_valid:
        return make_response(jsonify({"message": message}), status_code)
    return make_response(jsonify(mock_gacha_collection_list), 200)

""" ------------------ PLAYER ENDPOINTS ------------------ """

"""Player Collection Endpoints"""

@app.route('/api/player/gacha/player-collection', methods=['GET'])
@handle_errors
def get_gacha_collection():
    is_valid, message, status_code = mock_validate_token(request)
    if not is_valid:
        return make_response(jsonify({"message": message}), status_code)

    # Get user id from token
    auth_header = request.headers.get("Authorization")
    token = auth_header.removeprefix("Bearer ").strip()
    userId = extract_user_id_from_token(token)

    # get the player's gacha collection
    user_gacha_collection = [item for item in mock_gacha_collection_list if item['userId'] == userId]
    return make_response(jsonify(user_gacha_collection), 200)

@app.route('/api/player/gacha/player-collection/item/<int:collectionId>', methods=['GET'])
@handle_errors
def get_gacha_collection_details(collectionId):
    is_valid, message, status_code = mock_validate_token(request)
    if not is_valid:
        return make_response(jsonify({"message": message}), status_code)

    # get the player's gacha collection item
    gacha_collection_item = next((item for item in mock_gacha_collection_list if item['id'] == collectionId), None)
    if not gacha_collection_item:
        return make_response(jsonify({"message":"Gacha collection item not found"}), 404)
    return make_response(jsonify(gacha_collection_item), 200)

@app.route('/api/player/gacha/player-collection/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
def get_gacha_details(gachaId):
    is_valid, message, status_code = mock_validate_token(request)
    if not is_valid:
        return make_response(jsonify({"message": message}), status_code)
    
    # Get user id from token
    auth_header = request.headers.get("Authorization")
    token = auth_header.removeprefix("Bearer ").strip()
    userId = extract_user_id_from_token(token)

    # get the player's gacha collection
    user_gacha_collection = [item for item in mock_gacha_collection_list if item['userId'] == userId]

    # check if the gacha item is in the player's collection
    if not any(item['gachaId'] == gachaId for item in user_gacha_collection):
        return make_response(jsonify({"message":"Gacha item not found in player's collection"}), 404)
    
    # the gacha item is in the player's collection, get the details
    gacha_item = next((item for item in mock_gacha_list if item['id'] == gachaId), None)
    if not gacha_item:
        return make_response(jsonify({"message":"Gacha item not found"}), 404)

    return make_response(gacha_item, 200)

"""System Collection Endpoints"""

# Get full system gacha collection.
@app.route('/api/player/gacha/system-collection', methods=['GET'])
@handle_errors
def get_system_gacha_collection():
    is_valid, message, status_code = mock_validate_token(request)
    if not is_valid:
        return make_response(jsonify({"message": message}), status_code)

    return make_response(jsonify(mock_gacha_list), 200)

# Get details of a specific system gacha item.
@app.route('/api/player/gacha/system-collection/<int:gachaId>', methods=['GET'])
@handle_errors
def get_system_gacha_details(gachaId):
    gacha_item = next((item for item in mock_gacha_list if item['id'] == gachaId), None)
    if not gacha_item:
        return make_response(jsonify({"message":"Gacha item not found"}), 404)
    return make_response(jsonify(gacha_item), 200)

"""Gacha Roll Endpoints"""

# Roll a gacha
@app.route('/api/player/gacha/roll', methods=['POST'])
@handle_errors
def roll_gacha():
    is_valid, message, status_code = mock_validate_token(request)
    if not is_valid:
        return make_response(jsonify({"message": message}), status_code)

    # Check if the request contains JSON data
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)

    # Validate the JSON data
    is_valid, validation_message = is_valid_roll_data(json_data)
    if not is_valid:
        return make_response(jsonify({"message": validation_message}), 400)
    rarity_level = json_data["rarity_level"]
    
    # Get user id from token
    # auth_header = request.headers.get("Authorization")
    # token = auth_header.removeprefix("Bearer ").strip()
    # userId = extract_user_id_from_token(token)

    # # get the user data
    # user = next((item for item in mock_user_list if item['id'] == userId), None)
    # if not user:
    #     return make_response(jsonify({"message":"User not found"}), 404)

    # userIngameCurrency = user['ingameCurrency']

    # # check if the user has enough ingame currency to roll
    # roll_price = getattr(ROLL_PRICE,rarity_level)
    # if userIngameCurrency < roll_price:
    #     return make_response(jsonify({"message":"Insufficient in-game currency"}), 400)

    # Fetch all gacha items
    gacha_items = mock_gacha_list
    
    # Randomly select a gacha item
    selected_gacha = select_gacha(gacha_items, rarity_level)
    

    # add the gacha to the player's collection
    # gachacollection_item = {
    #     'id': len(mock_gacha_collection_list) + 1,
    #     'gachaId': selected_gacha['id'],
    #     'userId': userId,
    #     'timestamp': datetime.now().isoformat(),
    #     'source': 'ROLL'
    # }
    # mock_gacha_collection_list.append(gachacollection_item)

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

"""------------------ AUTH MOCK ENDPOINTS ------------------"""

SECRET_KEY = "mock_secret_key"  # Used for a simple hash/salt

@app.route('/api/player/login', methods=['POST'])
@handle_errors
def login_player():
    """Login a player."""
    json_data = request.get_json()

    # check if data is valid
    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)

    # if username and password != "user0", return an error
    if json_data["username"] != "user0" or json_data["password"] != "user0":
        return make_response(jsonify({"message":"Invalid username or password"}), 401)

    user_id = 1  # Hardcoded userId
    token = f"{user_id}:{SECRET_KEY}"  # Simple concatenation of userId and secret key
    
    return make_response(jsonify({"Access token": token}), 200)

@app.route('/api/admin/login', methods=['POST'])
@handle_errors
def login_admin():
    """Login a admin."""
    json_data = request.get_json()

    # check if data is valid
    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)

    # if username and password != "user0", return an error
    if json_data["username"] != "admin0" or json_data["password"] != "admin0":
        return make_response(jsonify({"message":"Invalid username or password"}), 401)

    user_id = 1  # Hardcoded userId
    token = f"{user_id}:{SECRET_KEY}"  # Simple concatenation of userId and secret key
    
    return make_response(jsonify({"Access token": token}), 200)

def extract_user_id_from_token(token):
    """
    Extracts the userId from a custom access token.
    """
    try:
        # Split the token to get the userId and verify the secret key
        user_id, secret = token.split(":")
        if secret != SECRET_KEY:
            raise ValueError("Invalid token")
        return int(user_id)
    except Exception as e:
        print(f"Error extracting userId: {e}")
        return 1 # Default to userId 1

def mock_validate_token(request):
    """
    Mock function to validate the token.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return False, "Missing Authorization header", 401
    token = auth_header.removeprefix("Bearer ").strip()
    if not token:
        return False, "Not authorized", 401

    return True, "Authorized", 200

def create_app():
    return app