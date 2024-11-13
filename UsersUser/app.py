import requests, time
from python_json_config import ConfigBuilder
from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound



builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 



@app.route('/api/player/profile/<int:user_id>', methods=['GET'])
def getPlayerInformation(user_id):
    try:
        response = requests.get(f'{config.urls.db_manager}/user/{user_id}')
        
        if response.status_code == 200:
            return make_response(jsonify(response.json()), 200)
        else:
            return make_response(jsonify({"error": "Player not found"}), response.status_code)
    except requests.RequestException as e:
        return make_response(jsonify({"error": "Failed to connect to database API", "details": str(e)}), 500)

@app.route('/api/player/update/<int:user_id>', methods=['PUT'])
def updatePlayerInformation(user_id):
    payload = request.json['profilePicture']
    if payload:
        response = requests.get(f'{config.urls.db_manager}/user/{user_id}')
        if response:
            status_data=response['status']
            ingameCurrency_data=response['ingameCurrency']
            update_data={
                'status':status_data,
                'ingameCurrency':ingameCurrency_data,
                'profilePicture':payload
            }
            update_response = requests.put(f'{config.urls.db_manager}/user/{user_id}', json=update_data)
            return update_response
    else:
        return make_response(jsonify({"error": "No profile picture provided"}), 400)


@app.route('/api/player/delete/<int:user_id>', methods=['DELETE'])
def delete_player(user_id):
    delete_response = requests.delete(f'{config.urls.db_manager}/user/{user_id}')  
    if delete_response.status_code == 200:
        return make_response(jsonify({"message": "Player successfully deleted"}), 200)
    elif delete_response.status_code == 500:
        return make_response(jsonify({"error": "Failed to delete player"}), 500)
    elif delete_response.status_code == 404:
        return make_response(jsonify({"error": "Player not found"}), 404)
    

