import requests, time, jsonify

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from python_json_config import ConfigBuilder
from datetime import datetime

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

def create_app():
    return app


# Configuration for the database manager service

@app.route('/api/player/currency/transaction-history/<int:user_id>', methods=['GET'])
def get_transaction_history(user_id):
    try:
        # Send a GET request to the database manager service to fetch transaction history
        response = requests.get(config.dbamangers.payment+ f'/currencytransaction/{user_id}')
        
        # Check if the request was successful
        if response.status_code == 200:
            transaction_history = response.json()
            return jsonify(transaction_history)

        elif response.status_code == 404:
            return make_response(jsonify({'error': 'Transactions not found'}), 404)

        elif response.status_code == 500:
            return make_response(jsonify({'error': 'Internal server error'}), 500)

        else:
            # Handle other unexpected status codes
            return make_response(jsonify({'error': f'Unexpected error: {response.status_code}'}), response.status_code)

    except requests.RequestException as e:
        # Handle errors that may occur during the HTTP request (e.g., network issues)
        return make_response(jsonify({'error': 'Failed to connect to the database manager service', 'details': str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/api/player/currency/purchase/', methods=['POST'])
def purchase_in_game_currency():
    try:
        # Extract data from request body
        data = request.get_json()
        in_game_currency = data.get('ingameAmount')
        user_id = data.get('userId')
        

        # Check if required fields are present
        if in_game_currency is None or user_id is None:
            return make_response(jsonify({'error': 'in_game_currency and user_id are required'}), 400)

        if in_game_currency <=0:     
            return make_response(jsonify({'error': 'in game currency must be greater than zero'}), 400)


        # Calculate the real amount of money based on the in-game currency and currency rate
        real_amount = in_game_currency * config.system_settings.gacha_roll_price

        # Define the payload to send to the database manager service
        payload = {
            'userId': user_id,
            'timeStamp': datetime.now(),
            'ingameAmount': in_game_currency,
            'realAmount': real_amount
        }

        # Send a POST request to the database manager service to process the purchase
        response = requests.post(config.dbmanagers.payment+f'/currencytransaction', json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:  # Assuming 200 for successful creation
            return make_response(jsonify({'message': 'Purchase successful', 'transaction': response.json()}), 200)

        elif response.status_code == 404:
            return make_response(jsonify({'error': 'User not found'}), 404)

        elif response.status_code == 400:
            return make_response(jsonify({'error': 'Invalid purchase request'}), 400)

        elif response.status_code == 500:
            return make_response(jsonify({'error': 'Internal server error at the database manager'}), 500)

        else:
            # Handle other unexpected status codes
            return make_response(jsonify({'error': f'Unexpected error: {response.status_code}'}), response.status_code)

    except requests.RequestException as e:
        # Handle errors that may occur during the HTTP request (e.g., network issues)
        return make_response(jsonify({'error': 'Failed to connect to the database manager service', 'details': str(e)}), 500)

    except KeyError as e:
        # Handle missing data in the request body
        return make_response(jsonify({'error': f'Missing key: {str(e)}'}), 400)

@app.route('/api/player/currency/decrease/<int:user_id>', methods=['PUT'])
def decrease_in_game_currency(user_id):
    try:
        # Extract the amount to be deducted from the request body
        data = request.get_json()
        amount = data.get('amount')

        # Check if the amount is provided and valid
        if amount is None:
            return make_response(jsonify({'error': 'amount is required'}), 400)
        elif amount <= 0:
            return make_response(jsonify({'error': 'amount must be greater than zero'}), 400)

        # Fetch the user's current balance from the database manager
        balance_response = requests.get(config.dbmanagers.user+ f'/user/{user_id}')

        
        if balance_response.status_code == 404:
            return make_response(jsonify({'error': 'User not found'}), 404)
        elif balance_response.status_code != 200:
            return make_response(jsonify({'error': 'Failed to retrieve user balance'}), 500)
        
        # Parse the balance data from the response
        user_data = balance_response.json()
        in_game_amount = user_data.get('ingameAmount')
        profile_picture= user_data.get('profilePicture')
        status=user_data.get('status')


        # Check if the amount exceeds the current balance
        if amount > in_game_amount:
            return make_response(jsonify({'error': 'Insufficient balance'}), 400)

        # Define the payload to send to the database manager service
        payload = {
            'status': status,
            'profilePicture': profile_picture,
            'ingameAmount': in_game_amount-amount
        }

        # Send a PUT request to the database manager service to decrease the balance
        response = requests.put(config.dbmanagers.user+f'/user/{user_id}', json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            return make_response(jsonify({'message': 'Balance decreased successfully', 'transaction': response.json()}), 200)

        elif response.status_code == 400:
            return make_response(jsonify({'error': 'Invalid decrease request'}), 400)

        elif response.status_code == 500:
            return make_response(jsonify({'error': 'Internal server error at the database manager'}), 500)

        else:
            # Handle other unexpected status codes
            return make_response(jsonify({'error': f'Unexpected error: {response.status_code}'}), response.status_code)

    except requests.RequestException as e:
        # Handle errors that may occur during the HTTP request (e.g., network issues)
        return make_response(jsonify({'error': 'Failed to connect to the database manager service', 'details': str(e)}), 500)

    except KeyError as e:
        # Handle missing data in the request body
        return make_response(jsonify({'error': f'Missing key: {str(e)}'}), 400)


@app.route('/api/player/currency/increase/<int:user_id>', methods=['PUT'])
def increase_currency(user_id):
    try:
        # Get the amount to increase from the JSON payload
        data = request.get_json()
        
        # Check if 'amount' is provided in the data
        if 'amount' not in data:
            return make_response(jsonify({'error': 'Amount field is required'}), 400)
        
        # Get the amount and ensure it is valid
        amount = data['amount']
        if amount <= 0:
            return make_response(jsonify({'error': 'Amount must be a positive number'}), 400)

        balance_response = requests.get(config.dbmanagers.user+ f'/user/{user_id}')
        
        if balance_response.status_code == 404:
            return make_response(jsonify({'error': 'User not found'}), 404)
        elif balance_response.status_code != 200:
            return make_response(jsonify({'error': 'Failed to retrieve user balance'}), 500)
        
        # Parse the balance data from the response
        user_data = balance_response.json()
        in_game_amount = user_data.get('ingameAmount')
        profile_picture= user_data.get('profilePicture')
        status=user_data.get('status')

        # Prepare the payload to send to the Database Manager service
        payload = {
            'status': status,
            'profilePicture': profile_picture,
            'ingameAmount': in_game_amount+amount
        }

        # Make a POST request to the database manager's /transactions endpoint
        response = requests.put(config.dbmanagers.user+f'/user/{user_id}', json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            return make_response(jsonify({'message': 'Currency increased successfully', 'user_id': user_id, 'amount': amount}), 200)
        else:
            # Handle errors from the database manager service
            return make_response(jsonify({'error': 'Failed to update balance on database manager service'}), 500)

    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)








