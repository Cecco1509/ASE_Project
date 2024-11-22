import requests, time

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from python_json_config import ConfigBuilder

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
app = Flask(__name__, instance_relative_config=True)

@app.route('/api/admin/users', methods=['GET'])
def get_players():
    try:
        response = requests.get(f'{config.dbmanagers.user}/user')
        if response.status_code == 200:
            return make_response(jsonify(response.json()), 200)
        else:
            return make_response(jsonify({"error": "Failed to fetch player data from the database API."}), 500)

    except requests.RequestException as e:
        return make_response(jsonify({"error": f"An error occurred while fetching data: {str(e)}"}), 500)



@app.route('/api/admin/users/<int:user_id>', methods=['GET'])
def get_player(user_id):
    try:
        response = requests.get(f'{config.dbmanagers.user}/user/{user_id}')
        if response.status_code == 200:
            return make_response(jsonify(response.json()), 200)
        else:
            return make_response(jsonify({"error": "Failed to fetch player's data from the database API."}), response.status_code)
    except requests.RequestException as e:
        return make_response(jsonify({"error": f"An error occurred while fetching data: {str(e)}"}), 500)


@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
def update_player(user_id):
    if 'profilePicture' in request.get_json():
        payload = request.json['profilePicture']
        response = requests.get(f'{config.dbmanagers.user}/user/{user_id}')
        if response.status_code==200:
            status_data=response['status']
            ingameCurrency_data=response['ingameCurrency']
            update_data={
                'status':status_data,
                'ingameCurrency':ingameCurrency_data,
                'profilePicture':payload
            }
            update_response = requests.put(f'{config.dbmanagers.user}/user/{user_id}', json=update_data)
            return update_response
        return make_response(jsonify({"error":"Unsuccessful data retrieval from the database manager/User ID non existent"}),response.status_code)
    return make_response(jsonify({"error": "No profile picture provided"}), 400)




@app.route('/api/admin/users/ban/<int:user_id>', methods=['POST'])
def ban_player(user_id):
    
    if 'status' in request.get_json():
        payload = request.json['status']
        response = requests.get(f'{config.dbmanagers.user}/user/{user_id}')
        if response.status_code==200:
            ingameCurrency_data=response['ingameCurrency']
            profilePicture_data=response['profilePicture']
            update_data={
                'status':payload,
                'ingameCurrency':ingameCurrency_data,
                'profilePicture':profilePicture_data
            }
            update_response = requests.put(f'{config.dbmanagers.user}/user/{user_id}', json=update_data)
            return update_response
        return make_response(jsonify({"error":"Unsuccessful data retrieval from the database manager/User ID non existent"}),response.status_code)
    return make_response(jsonify({"error": "No status provided"}), 400)



def create_app():
    return app