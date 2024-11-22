import requests, time

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from python_json_config import ConfigBuilder
from admin_mock import *
builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
app = Flask(__name__, instance_relative_config=True)

@app.route('/api/admin/users', methods=['GET'])
def get_players():
    response = getPlayers()
    if  response['status'] == 200:
        return make_response(jsonify(response['data']), response['status'])
    else:
        return make_response(jsonify({"error": "Players not found"}), response['status'])



@app.route('/api/admin/users/<int:user_id>', methods=['GET'])
def get_player(user_id):
    response = getPlayer(user_id)
    if  response['status'] == 200:
        return make_response(jsonify(response['data']), response['status'])
    else:
        return make_response(jsonify({"error": "Player not found"}), response['status'])


@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
def update_player(user_id):
    if 'profilePicture' in request.get_json():
        payload = request.json['profilePicture']
        response = getPlayer(user_id)
        response_json=response['data']
        if response['status']==200:
            status_data=response_json['status']
            ingameCurrency_data=response_json['ingameCurrency']
            update_data={
                'status':status_data,
                'ingameCurrency':ingameCurrency_data,
                'profilePicture':payload
            }
            update_response = updatePlayer()
            return make_response(jsonify(update_response),update_response['status'])
        return make_response(jsonify({"error":"Unsuccessful data retrieval from the database manager/User ID non existent"}),response['status'])
    return make_response(jsonify({"error": "No profile picture provided"}), 400)




@app.route('/api/admin/users/ban/<int:user_id>', methods=['POST'])
def ban_player(user_id):
    if 'status' in request.get_json():
        payload = request.json['status']
        response = getPlayer(user_id)
        response_json=response['data']
        if response['status']==200:
            profilePicture_data=response_json['profilePicture']
            ingameCurrency_data=response_json['ingameCurrency']
            update_data={
                'status':payload,
                'ingameCurrency':ingameCurrency_data,
                'profilePicture': profilePicture_data
            }
            update_response = banPlayer(user_id)
            return make_response(jsonify(update_response['data']),update_response['status'])
        return make_response(jsonify({"error":"Unsuccessful data retrieval from the database manager/User ID non existent"}),response['status'])
    return make_response(jsonify({"error": "No status provided"}), 400)



def create_app():
    return app