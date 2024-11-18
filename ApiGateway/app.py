import requests, time

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from python_json_config import ConfigBuilder
from handle_errors import handle_errors

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
GACHAS_ADMIN_URL = config.services.gachasadmin

@app.route('/api/admin/gacha', methods=['GET'])
@handle_errors
def admin_gacha():
    """Fetch all gacha items."""
    response = requests.get(GACHAS_ADMIN_URL + '/api/admin/gacha')
    response.raise_for_status()
    gacha_items = response.json()
    return make_response(jsonify(gacha_items), 200)

@app.route('/api/admin/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
def get_single_gacha(gachaId):
    """Fetch a single gacha item by ID."""
    response = requests.get(GACHAS_ADMIN_URL + f'/api/admin/gacha/{gachaId}')
    response.raise_for_status()
    return make_response(jsonify(response.json()), 200)
    
@app.route('/api/admin/gacha', methods=['POST'])
@handle_errors
def create_gacha():
    """Create a new gacha item."""
    json_data = request.get_json()

    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)

    response = requests.post(GACHAS_ADMIN_URL + '/api/admin/gacha', json=json_data)
    #response.raise_for_status()
    # i commented this line so the 400 error message will be returned the same, otherwise, the error message will be ovverriden
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/admin/gacha/<int:gachaId>', methods=['PUT'])
@handle_errors
def update_gacha(gachaId):
    """Update a gacha item."""
    json_data = request.get_json()

    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)

    response = requests.put(GACHAS_ADMIN_URL + f'/api/admin/gacha/{gachaId}', json=json_data)
    return make_response(jsonify(response.json()), 200)

# TODO: create separate files and import them here

def create_app():
    return app