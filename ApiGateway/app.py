import requests, time

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from python_json_config import ConfigBuilder

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

def create_app():
    return app

# Configuration for the database manager service
  # Replace with actual URL

@app.route('/api/player/currency<int:user_id>', methods=['GET'])
def get_transaction_history(user_id):
    
        # Send a GET request to the database manager service to fetch transaction history
        response = requests.get(config.urls.payments_player_microservice+f'/api/player/currency/{user_id}')
        return response


@app.route('/api/player/currency/', methods=['POST'])
def purchase_in_game_currency():
        # Prepare payload
        data = request.get_json()
        # Send request to microservice
        response = requests.post(f"{config.urls.payments_player_microservice}/api/player/currency/", json=data)
        # Forward the microservice's response to the user
        return response

@app.route('/api/player/decrease/<int:user_id>', methods=['PUT'])
def decrease_in_game_currency(user_id):
    
        # Extract the amount to be deducted from the request body
        data = request.get_json()
        
        response = requests.put(config.urls.payments_player_microservice+ f'/api/player/decrease/update_balance', json=data)
        
        return response


@app.route('/api/player/increase/<int:user_id>', methods=['PUT'])
def increase_currency(user_id):
    
        data = request.get_json()
        
        response = requests.put(config.urls.payments_player_microservice+ f'/api/player/increase/update_balance', json=data)

        return response