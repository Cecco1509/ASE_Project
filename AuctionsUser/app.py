import functools
import os
import threading
import requests, time
from flask import jsonify
from ..DBManager.models import Auction, Bids

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

def create_app():
    return app
