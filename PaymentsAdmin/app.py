import requests, time

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from python_json_config import ConfigBuilder

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

def create_app():
    return app


@app.route('/api/admin/currency/<int:user_id>', methods=['GET'])
def get_transaction_history(user_id):
    try:
        # Prepare the request URL for fetching transaction history
        transaction_history_url = config.dbmanagers.payment+f'/currencytransaction/{user_id}'
        

        # Make a GET request to the database manager service to fetch the transaction history
        response = requests.get(transaction_history_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Return the transaction history data
            return make_response(jsonify(response.json()), 200)
        elif response.status_code == 404: 
              return make_response(jsonify({'error': 'User not found'}), 404)
        else:
            # Handle errors from the database manager service
            return make_response(jsonify({'error': 'Failed to retrieve transaction history'}), 500)

    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True)