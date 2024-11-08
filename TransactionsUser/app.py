import requests, time

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

def create_app():
    return app