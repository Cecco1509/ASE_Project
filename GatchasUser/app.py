import requests, time
from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from handle_errors import handle_errors

app = Flask(__name__)

DB_MANAGER_GACHA_URL = 'http://dbmanager_gacha:5000'

@app.route('/api/player/gacha/player-collection/<int:user_id>', methods=['GET'])
@handle_errors
def get_player_collection(user_id):
    """Fetch player collection."""
    # Make a GET request to the DB manager service
    response = requests.get(DB_MANAGER_GACHA_URL + f'/gacha/player-collection/{user_id}')
    response.raise_for_status()

    gacha_items = response.json()
    return make_response(jsonify(gacha_items), 200)

def create_app():
    return app