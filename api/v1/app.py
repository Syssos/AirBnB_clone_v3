#!/usr/bin/python3
""" Flask App for AirBnB clone"""
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS
import os


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown(self):
    """ calls close to close session
    """
    storage.close()


@app.errorhandler(404)
def errorhandler(error):
    """ Returns status 404 Not found
    """
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    hosts = os.getenv("HBNB_API_HOST", default="0.0.0.0")
    ports = int(os.getenv("HBNB_API_PORT", default=5000))
    app.run(host=hosts, port=ports, threaded=True)
