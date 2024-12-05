import requests, time
from python_json_config import ConfigBuilder
from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 



@app.route('/api/player/profile', methods=['GET'])
def getPlayerInformation():
    auth_response = requests.get(config.services.authmicroservice + '/helloPlayer', headers=request.headers, verify=False)
    if auth_response.status_code != 200:
        return make_response(auth_response.json(), auth_response.status_code)  
    user_info_response = requests.get(config.services.authmicroservice + '/api/player/UserInfo', headers=request.headers, verify=False)
    if user_info_response.status_code != 200:
        return make_response(user_info_response.json(), user_info_response.status_code)  
    user_id=user_info_response['id']
    response = requests.get(f'{config.dbmanagers.user}/user/{user_id}', verify=False)
    if response.status_code == 200:
        return make_response(jsonify(response.json()), 200)
    else:
        return make_response(jsonify({"error": "Player not found"}), response.status_code)

@app.route('/api/player/update', methods=['PUT'])
def updatePlayerInformation():
    auth_response = requests.get(config.services.authmicroservice + '/helloPlayer', headers=request.headers, verify=False)
    if auth_response.status_code != 200:
        return make_response(auth_response.json(), auth_response.status_code) 
    user_info_response = requests.get(config.services.authmicroservice + '/api/player/UserInfo', headers=request.headers, verify=False)
    if user_info_response.status_code != 200:
        return make_response(user_info_response.json(), user_info_response.status_code)  
    user_id=user_info_response['id']
    if 'profilePicture' in request.get_json():
        payload = request.json['profilePicture']
        response = requests.get(f'{config.dbmanagers.user}/user/{user_id}', verify=False, timeout=config.timeout.medium)
        if response.status_code==200:
            status_data=response.json()['status']
            ingameCurrency_data=response.json()['ingameCurrency']
            update_data={
                'status':status_data,
                'ingameCurrency':ingameCurrency_data,
                'profilePicture':payload
            }
            update_response = requests.put(f'{config.dbmanagers.user}/user/{user_id}', json=update_data, verify=False, timeout=config.timeout.medium)
            return make_response(jsonify(update_response.json()), update_response.status_code)
        return make_response(jsonify({"error":"Unsuccessful data retrieval from the database manager/User ID non existent"}),response.status_code)
    return make_response(jsonify({"error": "No profile picture provided"}), 400)




@app.route('/api/player/delete', methods=['DELETE'])
def delete_player():
    auth_response = requests.get(config.services.authmicroservice + '/helloPlayer', headers=request.headers, verify=False)
    if auth_response.status_code != 200:
        return make_response(auth_response.json(), auth_response.status_code) 
    user_info_response = requests.get(config.services.authmicroservice + '/api/player/UserInfo', headers=request.headers, verify=False)
    if user_info_response.status_code != 200:
        return make_response(user_info_response.json(), user_info_response.status_code)  
    user_id=user_info_response['id']
    delete_response = requests.delete(f'{config.dbmanagers.user}/user/{user_id}', verify=False)  
    if delete_response.status_code == 200:
        delete_response = requests.delete(f'{config.services.authmicroservice}/api/player/{user_id}', verify=False, timeout=config.timeout.medium)  
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
    auth_response = requests.get(config.services.authmicroservice + '/helloAdmin', headers=request.headers, verify=False, timeout=config.timeout.medium)
    if auth_response.status_code != 200:
        return make_response(auth_response.json(), auth_response.status_code) 
    response = requests.get(f'{config.dbmanagers.user}/user', verify=False, timeout=config.timeout.medium)
    if response.status_code == 200:
        return make_response(jsonify(response.json()), 200)
    else:
        return make_response(jsonify({"error": "Players not found"}), response.status_code)


@app.route('/api/admin/users/<int:user_id>', methods=['GET'])
def get_player(user_id):
    auth_response = requests.get(config.services.authmicroservice + '/helloAdmin', headers=request.headers, verify=False, timeout=config.timeout.medium)
    if auth_response.status_code != 200:
        return make_response(auth_response.json(), auth_response.status_code) 
    response = requests.get(f'{config.dbmanagers.user}/user/{user_id}', verify=False, timeout=config.timeout.medium)
    if response.status_code == 200:
        return make_response(jsonify(response.json()), 200)
    else:
        return make_response(jsonify({"error": "Player not found"}), response.status_code)


@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
def update_player(user_id):
    auth_response = requests.get(config.services.authmicroservice + '/helloAdmin', headers=request.headers, verify=False, timeout=config.timeout.medium)
    if auth_response.status_code != 200:
        return make_response(auth_response.json(), auth_response.status_code) 
    if 'profilePicture' in request.get_json():
        payload = request.json['profilePicture']
        response = requests.get(f'{config.dbmanagers.user}/user/{user_id}', verify=False, timeout=config.timeout.medium)
        if response.status_code==200:
            status_data=response.json()['status']
            ingameCurrency_data=response.json()['ingameCurrency']
            update_data={
                'status':status_data,
                'ingameCurrency':ingameCurrency_data,
                'profilePicture':payload
            }
            update_response = requests.put(f'{config.dbmanagers.user}/user/{user_id}', json=update_data, verify=False, timeout=config.timeout.medium)
            return make_response(jsonify(update_response.json()),update_response.status_code)
        return make_response(jsonify({"error":"User not found."}),404)
    return make_response(jsonify({"error": "No profile picture provided"}), 400)




@app.route('/api/admin/users/ban/<int:user_id>', methods=['POST'])
def ban_player(user_id):
    auth_response = requests.get(config.services.authmicroservice + '/helloAdmin', headers=request.headers, verify=False, timeout=config.timeout.medium)
    if auth_response.status_code != 200:
        return make_response(auth_response.json(), auth_response.status_code) 
    if 'status' in request.get_json():
        payload = request.json['status']
        response = requests.get(f'{config.dbmanagers.user}/user/{user_id}', verify=False, timeout=config.timeout.medium)
        if response.status_code==200:
            ingameCurrency_data=response.json()['ingameCurrency']
            profilePicture_data=response.json()['profilePicture']
            update_data={
                'status':payload,
                'ingameCurrency':ingameCurrency_data,
                'profilePicture':profilePicture_data
            }
            update_response = requests.put(f'{config.dbmanagers.user}/user/{user_id}', json=update_data, verify=False)
            return make_response(jsonify(update_response.json()),update_response.status_code)
        return make_response(jsonify({"error":"User not found."}),404)
    return make_response(jsonify({"error": "No status provided"}), 400)


def create_app():
    return app