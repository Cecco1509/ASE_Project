import requests, time

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from handle_errors import handle_errors
from auth_utils import *
from python_json_config import ConfigBuilder
from transactions_mock_db import *

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 


@app.route('/api/admin/market-transaction/<int:user_id>', methods=['GET'])
@handle_errors
def get_player_transaction_history_admin(user_id):
    try:

        return make_response(jsonify([transaction for transaction in mock_transactions if transaction['sellerId'] == user_id
                                                                            and transaction["buyerId"] == user_id]), 200)
    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 500)

@app.route('/api/player/market-transaction', methods=['GET'])
@handle_errors
def get_player_transaction_history():
    try:
        return make_response(jsonify([transaction for transaction in mock_transactions if transaction['sellerId'] == 1
                                                                            and transaction["buyerId"] == 1]), 200)
    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 500)

@app.route('/api/admin/login', methods=['POST'])
def login_admin():
    return make_response(jsonify({"Access token" : ""}), 200)

@app.route('/api/player/login', methods=['POST'])
def login_player():
    return make_response(jsonify({"Access token" : ""}), 200)

def create_app():
    return app