from functools import wraps
from flask import jsonify, make_response
import requests

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 404:
                # Handle 404 error (resource not found)
                return make_response(jsonify({"error": "Resource not found"}), 404)
            elif http_err.response.status_code == 500:
                # Handle 500 error (internal server error)
                return make_response(jsonify({"error": "Internal server error occurred"}), 500)
            else:
                # General HTTP error message for other status codes (e.g., 400, 403, etc.)
                return make_response(jsonify({"error": f"HTTP error occurred: {http_err}"}), http_err.response.status_code)
        except requests.exceptions.ConnectionError as _:
            return make_response(jsonify({"error": "Connection error. Please try again later."}), 503)
        except requests.exceptions.Timeout as _:
            return make_response(jsonify({"error": "The request timed out. Please try again later."}), 504)
        except Exception as err:
            # Catch any other exceptions
            return make_response(jsonify({"error": f"An unexpected error occurred: {err}"}), 500) 
    return wrapper