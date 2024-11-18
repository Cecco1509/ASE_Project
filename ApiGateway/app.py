import requests, time

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from python_json_config import ConfigBuilder

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
GACHAS_ADMIN_URL = config.services.gachasadmin

@app.route('/api/admin/gacha', methods=['GET'])
def admin_gacha():
    try:
        response = requests.get(GACHAS_ADMIN_URL + '/api/admin/gacha')
        response.raise_for_status()
        gacha_items = response.json()
        return make_response(jsonify(gacha_items), 200)
    except Exception as e:
        return make_response(jsonify({"error": f"APIGateway: An unexpected error occurred: {e}"}), 400)
    
@app.route('/api/admin/gacha', methods=['POST'])
def create_gacha():
    try:
        json_data = request.get_json()
        if json_data:
            response = requests.post(GACHAS_ADMIN_URL + '/api/admin/gacha', json=json_data)
            response.raise_for_status()
            return make_response(jsonify(response.json()), 200)
        return make_response(jsonify({"message":"Invalid gacha data"}), 400)
    except Exception as e:
        return make_response(jsonify({"error": f"APIGateway: An unexpected error occurred: {e}"}), 400)

# TODO: create separate files and import them here

def create_app():
    return app