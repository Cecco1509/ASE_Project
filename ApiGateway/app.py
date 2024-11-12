import requests, time

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

def create_app():
    return app

    CURRENCY_ADMIN_URL = 'http://paymentsadmin:5000'

@app.route('/api/admin/currency/<int:user_id>', methods=['GET'])
def get_transaction_history(user_id):
    
        response = requests.get(CURRENCY_ADMIN_URL+f'/api/admin/currency/{user_id}')
        return response

       