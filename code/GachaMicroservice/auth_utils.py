from functools import wraps
from flask import request, make_response, jsonify
import requests
from python_json_config import ConfigBuilder

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
AUTH_MICROSERVICE_URL = config.services.authmicroservice

def validate_player_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Call the auth service to validate the token
        auth_response = requests.get(AUTH_MICROSERVICE_URL + '/helloPlayer', headers=request.headers, verify=False, timeout=config.timeout.medium)
        
        # If the authentication fails, return Unauthorized response
        if auth_response.status_code != 200:
            return make_response(jsonify({"message": "Unauthorized"}), 401)
        
        # Optionally, we can pass the auth_response to the view function if needed
        # For example, we could add it to kwargs
        kwargs['auth_response'] = auth_response
        
        # Proceed to the actual view function
        return f(*args, **kwargs)
    
    return decorated_function

def validate_admin_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Call the auth service to validate the admin's token
        auth_response = requests.get(AUTH_MICROSERVICE_URL + '/helloAdmin', headers=request.headers, verify=False, timeout=config.timeout.medium)
        
        # If the authentication fails, return Unauthorized response
        if auth_response.status_code != 200:
            return make_response(jsonify({"message": "Unauthorized"}), 401)
        
        # Proceed to the actual view function (no need to pass auth_response)
        return f(*args, **kwargs)
    
    return decorated_function