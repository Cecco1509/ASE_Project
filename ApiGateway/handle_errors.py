from functools import wraps
from flask import jsonify, make_response
import requests

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as http_err:
            return make_response(jsonify({"error": f"HTTP error occurred: {http_err}"}), 400)
        except requests.exceptions.ConnectionError as conn_err:
            return make_response(jsonify({"error": "Connection error. Please try again later."}), 503)
        except requests.exceptions.Timeout as timeout_err:
            return make_response(jsonify({"error": "The request timed out. Please try again later."}), 504)
        except Exception as err:
            # Catch any other exceptions
            return make_response(jsonify({"error": f"An unexpected error occurred: {err}"}), 500)
    return wrapper
