import requests, time

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

def create_app():
    return app

USERS_USER_URL="http://usersuser:5000"

@app.route('/api/player/profile/<int:user_id>', methods=['GET'])
def getPlayerInformation(user_id):
    try:
        response = requests.get(f'{USERS_USER_URL}/api/player/profile/{user_id}')
        
        if response.status_code == 200:
            return make_response(jsonify(response.json()), 200)
        else:
            return make_response(jsonify({"error": "Player not found"}), response.status_code)
    except requests.RequestException as e:
        return make_response(jsonify({"error": "Failed to connect to database API", "details": str(e)}), 500)

@app.route('/api/player/update/<int:user_id>', methods=['PUT'])
def updatePlayerInformation(user_id):
    payload=request.get_json()
    response=requests.put(f'{USERS_USER_URL}/api/player/update/{user_id}',json=payload)
    return response

@app.route('/api/player/delete/<int:user_id>', methods=['DELETE'])
def delete_player(user_id):
    delete_response = requests.delete(f'{USERS_USER_URL}/api/player/delete/{user_id}')
    return delete_response
    
