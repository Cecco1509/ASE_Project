import requests, time

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

def create_app():
    return app

# Configuration for the database manager service
CURRENCY_PLAYER_URL = 'http://paymentsuser:5000'  # Replace with actual URL

@app.route('/api/player/currency<int:user_id>', methods=['GET'])
def get_transaction_history(user_id):
    
        # Send a GET request to the database manager service to fetch transaction history
        response = requests.get(CURRENCY_PLAYER_URL+f'/api/player/currency/{user_id}')
        return response


@app.route('/api/player/currency/', methods=['POST'])
def purchase_in_game_currency():
        # Prepare payload
        data = request.get_json()
        # Send request to microservice
        response = requests.post(f"{CURRENCY_PLAYER_URL}/api/player/currency/", json=data)
        # Forward the microservice's response to the user
        return response

@app.route('/api/player/decrease/<int:user_id>', methods=['PUT'])
def decrease_in_game_currency(user_id):
    
        # Extract the amount to be deducted from the request body
        data = request.get_json()
        
        response = requests.put(CURRENCY_PLAYER_URL+ f'/api/player/decrease/update_balance', json=data)
        
        return response


@app.route('/api/player/increase/<int:user_id>', methods=['PUT'])
def increase_currency(user_id):
    
        data = request.get_json()
        
        response = requests.put(CURRENCY_PLAYER_URL+ f'/api/player/increase/update_balance', json=data)

        return response