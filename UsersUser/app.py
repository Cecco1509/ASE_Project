import requests, time

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

def create_app():
    return app

@app.route('/api/player/profile/<int:user_id>', methods=['GET'])
def getPlayerInformation(user_id):
    try:
        response = requests.get({DATABASE_API_URL}/{user_id})
        
        if response.status_code == 200:
            return make_response(jsonify(response.json()), 200)
        else:
            return make_response(jsonify({"error": "Player not found"}), response.status_code)
    except requests.RequestException as e:
        return make_response(jsonify({"error": "Failed to connect to database API", "details": str(e)}), 500)

@app.route('/api/player/update/<int:user_id>', methods=['PUT'])
def updatePlayerInformation(user_id):
    new_profile_pic = request.json['profile_pic']
    if 'profile_pic' not in request.json:
        return make_response(jsonify({"error": "No profile picture provided"}), 400)

    response = requests.get(f"{DATABASE_API_URL}/{user_id}")

    if response.status_code == 404:
        return make_response(jsonify({"error": "Player not found"}), 404)
    elif response.status_code==500:
        return make_response(jsonify({"error":"While updating user"}), 500)


    update_data = {
        'profile_pic': new_profile_pic
    }
    update_response = requests.put(f"{DATABASE_API_URL}/{user_id}", json=update_data)

    if update_response.status_code == 200:
        updated_player = update_response.json()
        return make_response(jsonify(updated_player), 200)
    else:
        return make_response(jsonify({"error": "Failed to update profile picture"}), 500)

@app.route('api/player/delete/<int:user_id>', methods=['DELETE'])
def delete_player(user_id):
    response = requests.get(f"{DATABASE_API_URL}/{user_id}")
    
    delete_response = requests.delete(f"{DATABASE_API_URL}/{user_id}")
    
    if delete_response.status_code == 200:
        return make_response(jsonify({"message": "Player successfully deleted"}), 200)
    elif delete_response.status_code == 500:
        return make_response(jsonify({"error": "Failed to delete player"}), 500)
    elif delete_response.status_code == 404:
        return make_response(jsonify({"error": "Player not found"}), 404)
    

