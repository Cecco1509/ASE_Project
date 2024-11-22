import requests, time

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from python_json_config import ConfigBuilder
from paymentsadmin_mock import *


builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

def create_app():
    return app


@app.route('/api/admin/currency/<int:userId>', methods=['GET'])
def get_transaction_history(userId):
    try:
        # Prepare the request URL for fetching transaction history
        response = get_history(userId)
        

        # Make a GET request to the database manager service to fetch the transaction history
        

        # Check if the request was successful
        if response['status'] == 200:
            # Return the transaction history data
            return make_response(jsonify(response['data']), 200)
        elif response['status'] == 404: 
              return make_response(jsonify({'error': 'User not found'}), 404)    
        else:
            # Handle errors from the database manager service
            return make_response(jsonify({'error': 'Failed to retrieve transaction history'}), 500)

    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True)