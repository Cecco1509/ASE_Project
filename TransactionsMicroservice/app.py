import requests

from flask import Flask, make_response 
from handle_errors import handle_errors
from auth_utils import *
from python_json_config import ConfigBuilder

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 


builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

@app.route('/api/admin/market-transaction/<int:user_id>', methods=['GET'])
@handle_errors
@validate_admin_token
def get_player_transaction_history_admin(user_id, auth_response=None):
    try:
        response = requests.get(config.dbmanagers.transaction + f"/auctiontransaction/user/{user_id}", timeout=config.timeout.medium,verify=False)
        response.raise_for_status()

        return make_response(response.json(), 200)
    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 500)

@app.route('/api/player/market-transaction', methods=['GET'])
@handle_errors
@validate_player_token
def get_player_transaction_history(auth_response=None):
    try:
        response = requests.get(config.dbmanagers.transaction + f"/auctiontransaction/user/{auth_response["userId"]}", timeout=config.timeout.medium,verify=False)
        response.raise_for_status()

        return make_response(response.json(), 200)
    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 500)

def create_app():
    return app