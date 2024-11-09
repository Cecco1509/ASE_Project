import requests
from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from models import GachaItem

app = Flask(__name__)

DB_MANAGER_GACHA_URL = 'http://dbmanager_gacha:5000'

@app.route('/api/admin/gacha', methods=['GET'])
def get_all_gacha():
    """Fetch all gacha items."""
    try:
        # Make a GET request to the DB manager service
        response = requests.get(DB_MANAGER_GACHA_URL + f'/gacha')
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        gacha_items = response.json()
        return make_response(jsonify(gacha_items), 200)
    except Exception as err:
        # TODO better handle errors
        return make_response(jsonify({"error": f"GatchaAdmin: An unexpected error occurred: {err}"}), 400)
    
@app.route('/api/admin/gacha', methods=['POST'])
def add_gacha():
    """Add a new gacha item."""
    data = request.get_json()
    print(f"GatchaAdmin: Adding gacha item {data}")
    if data:
        try:
            # Make a POST request to the DB manager service
            response = requests.post(DB_MANAGER_GACHA_URL + f'/gacha', json=data)
            response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
            return make_response(jsonify({"message": f"GatchaAdmin: Gacha item added successfully"}), 200)
        except Exception as err:
            # TODO better handle errors
            return make_response(jsonify({"error": f"GatchaAdmin: An unexpected error occurred: {err}"}), 400)
    return make_response(jsonify({"error": "Missing JSON data"}), 400)

@app.route('/api/admin/gacha/<int:gacha_id>', methods=['DELETE'])
def delete_gacha(gacha_id):
    """Delete a gacha item."""
    try:
        # Make a DELETE request to the DB manager service
        response = requests.delete(DB_MANAGER_GACHA_URL + f'/gacha/{gacha_id}')
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        return make_response(jsonify({"message": f"GatchaAdmin: Gacha item {gacha_id} deleted successfully"}), 200)
    except Exception as err:
        # TODO better handle errors
        return make_response(jsonify({"error": f"GatchaAdmin: An unexpected error occurred: {err}"}), 400)

@app.route('/api/admin/gacha/<int:gacha_id>', methods=['PATCH'])
def update_gacha(gacha_id):
    """Update a gacha item."""
    data = request.get_json()
    print(f"GatchaAdmin: Updating gacha item {gacha_id} with data {data}")
    if data:
        try:
            # Make a PUT request to the DB manager service
            response = requests.patch(DB_MANAGER_GACHA_URL + f'/gacha/{gacha_id}', json=data)
            response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
            return make_response(jsonify({"message": f"GatchaAdmin: Gacha item {gacha_id} updated successfully"}), 200)
        except Exception as err:
            # TODO better handle errors
            return make_response(jsonify({"error": f"GatchaAdmin: An unexpected error occurred: {err}"}), 400)
    return make_response(jsonify({"error": "Missing JSON data"}), 400)

def create_app():
    return app