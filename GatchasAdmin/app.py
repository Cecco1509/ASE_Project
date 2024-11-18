import requests, time

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from python_json_config import ConfigBuilder

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
DB_MANAGER_GACHA_URL = config.dbmanagers.gacha

@app.route('/api/admin/gacha', methods=['GET'])
def get_all_gacha():
    """Fetch all gacha items."""
    try:
        response = requests.get(DB_MANAGER_GACHA_URL + f'/gacha')
        response.raise_for_status()
        gacha_items = response.json()
        return make_response(jsonify(gacha_items), 200)
    except Exception as e:
        return make_response(jsonify({"error": f"GatchaAdmin: An unexpected error occurred: {e}"}), 400)

# TODO: add error handler
# TODO: validate input
@app.route('/api/admin/gacha', methods=['POST'])
def create_gacha():
    """Create a new gacha item."""
    try:
        json_data = request.get_json()
        if json_data:
            response = requests.post(DB_MANAGER_GACHA_URL + f'/gacha', json=json_data)
            response.raise_for_status()
            return make_response(jsonify(response.json()), 200)
        return make_response(jsonify({"message":"Invalid gacha data"}), 400)
    except Exception as e:
        return make_response(jsonify({"error": f"GatchaAdmin: An unexpected error occurred: {e}"}), 400)

def create_app():
    return app