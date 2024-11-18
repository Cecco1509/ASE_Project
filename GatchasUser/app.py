import requests
from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from python_json_config import ConfigBuilder
from handle_errors import handle_errors
from datetime import datetime

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
DB_MANAGER_GACHA_URL = config.dbmanagers.gacha

"""Get player's gacha collection."""
@app.route('/api/player/gacha/player-collection/<int:userId>', methods=['GET'])
@handle_errors
def get_gacha_collection(userId):
    response = requests.get(f'{DB_MANAGER_GACHA_URL}/gachacollection/{userId}')
    response.raise_for_status()
    return make_response(response.json(), 200)

"""Create a new gacha collection item."""
@app.route('/api/player/gacha/player-collection', methods=['POST'])
@handle_errors
def create_gacha_collection():
    json_data = request.get_json()

    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)
    
    is_valid, validation_message = is_valid_gacha_collection_data(json_data)
    if not is_valid:
        return make_response(jsonify({"message": validation_message}), 400)
    
    # Add timestamp to the json data
    timestamp = datetime.utcnow().isoformat()
    json_data['timestamp'] = timestamp

    response = requests.post(f'{DB_MANAGER_GACHA_URL}/gachacollection', json=json_data)
    return make_response(jsonify(response.json()), response.status_code)

def is_valid_gacha_collection_data(data):
    """
    Validate the input JSON data for creating a gacha collection item.
    Checks for required fields, data types, and formats.
    """
    required_fields = {
        "gachaId": int,
        "userId": int,
        "source": str,
    }

    for field, expected_type in required_fields.items():
        if field not in data:
            return False, f"Missing required field: {field}"
        if not isinstance(data[field], expected_type):
            return False, f"Invalid type for field '{field}': Expected {expected_type.__name__}"

    return True, "Data is valid"

def create_app():
    return app