from flask import Flask, request, make_response, jsonify
from handle_errors import handle_errors
from datetime import datetime
import random
from gacha_mock_db import *

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

""" ------------------ ADMIN ENDPOINTS ------------------ """

@app.route('/api/admin/gacha', methods=['GET'])
@handle_errors
def get_all_gacha():
    """Fetch all gacha items."""
    return make_response(jsonify(mock_gacha_list), 200)

"""Fetch a single gacha item by ID."""
@app.route('/api/admin/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
def get_single_gacha(gachaId):
    # cbeck if gachaId is valid
    if gachaId < 1 or gachaId > len(mock_gacha_list):
        return make_response(jsonify({"message": f"Gacha item with ID {gachaId} not found"}), 404)
    return make_response(jsonify(mock_gacha_list[gachaId-1]), 200)

@app.route('/api/admin/gacha', methods=['POST'])
@handle_errors
def create_gacha():
    """Create a new gacha item."""
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
    global mock_gacha_list

    # check if gachaId is valid
    gacha_item = next((gacha for gacha in mock_gacha_list if gacha['id'] == gachaId), None)
    if not gacha_item:
        return make_response(jsonify({"message": f"Gacha item with ID {gachaId} not found"}), 404)
    
    # all data is valid, delete the gacha item from the mock list
    mock_gacha_list = [gacha for gacha in mock_gacha_list if gacha['id'] != gachaId]

    return make_response({"message":"Gacha sucessfully deleted."}, 200)

@app.route('/api/admin/gachacollection', methods=['GET'])
@handle_errors
def get_all_gachacollections():
    """Get all gacha collections."""
    return make_response(jsonify(mock_gacha_collection_list), 200)

""" ------------------ PLAYER ENDPOINTS ------------------ """

"""Player Collection Endpoints"""

@app.route('/api/player/gacha/player-collection/<int:userId>', methods=['GET'])
@handle_errors
def get_gacha_collection(userId):
    # get the player's gacha collection
    user_gacha_collection = [item for item in mock_gacha_collection_list if item['userId'] == userId]
    return make_response(jsonify(user_gacha_collection), 200)

@app.route('/api/player/gacha/player-collection/item/<int:collectionId>', methods=['GET'])
@handle_errors
def get_gacha_collection_details(collectionId):
    # get the player's gacha collection item
    gacha_collection_item = next((item for item in mock_gacha_collection_list if item['id'] == collectionId), None)
    if not gacha_collection_item:
        return make_response(jsonify({"message":"Gacha collection item not found"}), 404)
    return make_response(jsonify(gacha_collection_item), 200)

@app.route('/api/player/gacha/player-collection/<int:userId>/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
def get_gacha_details(userId, gachaId):
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
    json_data = request.get_json()

    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)
    
    is_valid, validation_message = is_valid_roll_data(json_data)
    if not is_valid:
        return make_response(jsonify({"message": validation_message}), 400)
    
    # get the user data
    userId = json_data['userId']
    user = next((item for item in mock_user_list if item['id'] == userId), None)

    if not user:
        return make_response(jsonify({"message":"User not found"}), 404)

    userIngameCurrency = user['ingameCurrency']

    # check if the user has enough ingame currency to roll
    if userIngameCurrency < ROLL_PRICE:
        return make_response(jsonify({"message":"Insufficient in-game currency"}), 400)
    
    # get a random gacha from the system collection
    random_gacha = random.choice(mock_gacha_list)

    # deduct the roll price from the user's in-game currency
    userIngameCurrency -= ROLL_PRICE

    # update the user's in-game currency
    user['ingameCurrency'] = userIngameCurrency

    # update the user data in the mock list
    for i, item in enumerate(mock_user_list):
        if item['id'] == userId:
            mock_user_list[i] = user
            break
    

    # add the gacha to the player's collection
    gachacollection_item = {
        'id': len(mock_gacha_collection_list) + 1,
        'gachaId': random_gacha['id'],
        'userId': userId,
        'timestamp': datetime.now().isoformat(),
        'source': 'ROLL'
    }
    mock_gacha_collection_list.append(gachacollection_item)

    # create a response json with the gachacollection id
    response_json = {
        'collectionId': gachacollection_item['id']
    }
    return make_response(response_json, 200)

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