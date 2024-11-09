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

def create_app():
    return app