from flask import Flask, request, make_response, jsonify
from handle_errors import handle_errors
from datetime import datetime
import random

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

ROLL_PRICE = 100

mock_gacha_list = [
        {
            'id': 1,
            'name': 'Gacha 1',
            'description': 'Description for Gacha 1',
            'image': 'image1.png',
            'rarityPercent': 25.9
        },
        {
            'id': 2,
            'name': 'Gacha 2',
            'description': 'Description for Gacha 2',
            'image': 'image2.png',
            'rarityPercent': 0.7
        },
        {
            'id': 3,
            'name': 'Gacha 3',
            'description': 'Description for Gacha 3',
            'image': 'image3.png',
            'rarityPercent': 57.3
        }
    ]

mock_gacha_collection_list = [
        {
            'id': 1,
            'gachaId': 1,
            'userId': 1,
            'timestamp': '2021-07-01T12:00:00',
            'source': 'ROLL'
        },
        {
            'id': 2,
            'gachaId': 2,
            'userId': 1,
            'timestamp': '2021-07-01T12:01:00',
            'source': 'AUCTION'
        },
        {
            'id': 3,
            'gachaId': 3,
            'userId': 2,
            'timestamp': '2021-07-01T12:02:00',
            'source': 'ROLL'
        }
    ]

mock_user_list = [
        {
            'id': 1,
            'authId': 101,
            'ingameCurrency': 1500.0,
            'profilePicture': 'profile1.png',
            'registrationDate': '2021-01-01T10:00:00',
            'status': 'ACTIVE'
        },
        {
            'id': 2,
            'authId': 102,
            'ingameCurrency': 3000.0,
            'profilePicture': 'profile2.png',
            'registrationDate': '2021-02-01T11:00:00',
            'status': 'ACTIVE'
        },
        {
            'id': 3,
            'authId': 103,
            'ingameCurrency': 500.0,
            'profilePicture': 'profile3.png',
            'registrationDate': '2021-03-01T12:00:00',
            'status': 'ACTIVE'
        }
    ]

"""Player Collection Endpoints"""

# Get player's gacha collection.
@app.route('/api/player/gacha/player-collection/<int:userId>', methods=['GET'])
@handle_errors
def get_gacha_collection(userId):
    # get the player's gacha collection
    user_gacha_collection = [item for item in mock_gacha_collection_list if item['userId'] == userId]
    return make_response(jsonify(user_gacha_collection), 200)

# Get player's gacha collection item
@app.route('/api/player/gacha/player-collection/item/<int:collectionId>', methods=['GET'])
@handle_errors
def get_gacha_collection_details(collectionId):
    # get the player's gacha collection item
    gacha_collection_item = next((item for item in mock_gacha_collection_list if item['id'] == collectionId), None)
    if not gacha_collection_item:
        return make_response(jsonify({"message":"Gacha collection item not found"}), 404)
    return make_response(jsonify(gacha_collection_item), 200)

# Get player's gacha item details
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