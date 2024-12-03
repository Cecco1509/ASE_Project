import requests, time

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from handle_errors import handle_errors
from auth_utils import *

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 


@app.route('/player/', methods=['GET'])
@handle_errors
@validate_player_token
def get_player_transaction_history():
    return make_response({"message": "OK"}, 200)


def create_app():
    return app