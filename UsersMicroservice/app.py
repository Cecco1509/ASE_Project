import requests, time
from python_json_config import ConfigBuilder
from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound



builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 



@app.route('/api/player/profile/<int:user_id>', methods=['GET'])
def getPlayerInformation(user_id):
    response = requests.get(f'{config.dbmanagers.user}/user/{user_id}')
    if response.status_code == 200:
        return make_response(jsonify(response.json()), 200)
    else:
        return make_response(jsonify({"error": "Player not found"}), response.status_code)

@app.route('/api/player/update/<int:user_id>', methods=['PUT'])
def updatePlayerInformation(user_id):
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




@app.route('/api/player/delete/<int:user_id>', methods=['DELETE'])
def delete_player(user_id):
    delete_response = requests.delete(f'{config.dbmanagers.user}/user/{user_id}')  
    if delete_response.status_code == 200:
        delete_response = requests.delete(f'{config.services.authmicroservice}/player/{user_id}')  
        if delete_response.status_code ==200:
            return make_response(jsonify({"message": "Player successfully deleted"}), 200)
        else:
            return make_response(jsonify({"error": "Player not found"}), 404)
    elif delete_response.status_code == 500:
        return make_response(jsonify({"error": "Failed to delete player"}), 500)
    elif delete_response.status_code == 404:
        return make_response(jsonify({"error": "Player not found"}), 404)
    

@app.route('/api/admin/users', methods=['GET'])
def get_players():
    response = requests.get(f'{config.dbmanagers.user}/user')
    if response.status_code == 200:
        return make_response(jsonify(response.json()), 200)
    else:
        return make_response(jsonify({"error": "Players not found"}), response.status_code)


@app.route('/api/admin/users/<int:user_id>', methods=['GET'])
def get_player(user_id):
    response = requests.get(f'{config.dbmanagers.user}/user/{user_id}')
    if response.status_code == 200:
        return make_response(jsonify(response.json()), 200)
    else:
        return make_response(jsonify({"error": "Player not found"}), response.status_code)


@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
def update_player(user_id):
    if 'profilePicture' in request.get_json():
        payload = request.json['profilePicture']
        response = requests.get(f'{config.dbmanagers.user}/user/{user_id}')
        response_data=response.json()
        if response.status_code==200:
            status_data=response_data['status']
            ingameCurrency_data=response_data['ingameCurrency']
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