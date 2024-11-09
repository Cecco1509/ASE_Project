import requests, time

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

app = Flask(__name__)

GACHAS_ADMIN_URL = 'http://gachasadmin:5000'

@app.route('/api/admin/gacha', methods=['GET'])
def admin_gacha():
    try:
        response = requests.get(GACHAS_ADMIN_URL + '/api/admin/gacha')
        response.raise_for_status()
        gacha_items = response.json()
        return make_response(jsonify(gacha_items), 200)
    except Exception as err:
        return make_response(jsonify({"error": f"APIGateway: An unexpected error occurred: {err}"}), 400)

def create_app():
    return app