import requests, time

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from handle_errors import handle_errors

app = Flask(__name__)

GACHAS_ADMIN_URL = 'http://gachasadmin:5000'
GACHAS_PLAYER_URL = 'http://gachasuser:5000'

"""ADMIN API"""
"""GahcaAdmin API"""
@app.route('/api/admin/gacha', methods=['GET'])
def admin_gacha():
    try:
        response = requests.get(GACHAS_ADMIN_URL + '/api/admin/gacha')
        response.raise_for_status()
        gacha_items = response.json()
        return make_response(jsonify(gacha_items), 200)
    except Exception as err:
        return make_response(jsonify({"error": f"APIGateway: An unexpected error occurred: {err}"}), 400)
    
@app.route('/api/admin/gacha', methods=['POST'])
def admin_gacha_add():
    data = request.get_json()
    print(f"APIGateway: Adding gacha item {data}")
    if data:
        try:
            response = requests.post(GACHAS_ADMIN_URL + '/api/admin/gacha', json=data)
            response.raise_for_status()
            return make_response(jsonify(response.json()), 200)
        except Exception as err:
            return make_response(jsonify({"error": f"APIGateway: An unexpected error occurred: {err}"}), 400)
    return make_response(jsonify({"error": "APIGateway: Missing JSON data"}), 400)

@app.route('/api/admin/gacha/<int:gacha_id>', methods=['DELETE'])
def admin_gacha_delete(gacha_id):
    try:
        response = requests.delete(GACHAS_ADMIN_URL + f'/api/admin/gacha/{gacha_id}')
        response.raise_for_status()
        return make_response(jsonify({"message": f"APIGateway: Gacha item {gacha_id} deleted successfully"}), 200)
    except Exception as err:
        return make_response(jsonify({"error": f"APIGateway: An unexpected error occurred: {err}"}), 400)

@app.route('/api/admin/gacha/<int:gacha_id>', methods=['PATCH'])
def admin_gacha_update(gacha_id):
    data = request.get_json()
    print(f"APIGateway: Updating gacha item {gacha_id} with data {data}")
    if data:
        try:
            response = requests.patch(GACHAS_ADMIN_URL + f'/api/admin/gacha/{gacha_id}', json=data)
            response.raise_for_status()
            return make_response(jsonify(response.json()), 200)
        except Exception as err:
            return make_response(jsonify({"error": f"APIGateway: An unexpected error occurred: {err}"}), 400)
    return make_response(jsonify({"error": "APIGateway: Missing JSON data"}), 400)

"""PLAYER API"""
"""GatchaUser API"""
@app.route('/api/player/gacha/player-collection/<int:user_id>', methods=['GET'])
@handle_errors
def get_player_collection(user_id):
    print(f"APIGateway: Fetching player collection for user {user_id}")
    response = requests.get(GACHAS_PLAYER_URL + f'/api/player/gacha/player-collection/{user_id}')
    response.raise_for_status()
    gacha_items = response.json()
    return make_response(jsonify(gacha_items), 200)

def create_app():
    return app