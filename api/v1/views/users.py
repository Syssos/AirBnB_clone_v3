#!/usr/bin/python3
"""City objects that handles all default RestFul API actions"""


from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models import Amenity
from models import City
from models import Place
from models import Review
from models import State
from models import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """ returns state info
    """
    emli = []
    stateinfo = storage.all('User')
    for key, value in stateinfo.items():
        usr = value.to_dict()
        emli.append(usr)
    return jsonify(emli)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Retrieves a City object
    """
    vari = storage.get('User', user_id)
    if vari is None:
        abort(404)
    return jsonify(vari.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Returns info for <state_id>
    """
    var_obj = storage.get('User', user_id)
    if var_obj is None:
        abort(404)
    var_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """ Adds a new state to State
    """
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in request.json:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in request.json:
        return jsonify({'error': 'Missing password'}), 400
    news = request.get_json()
    newo = User(email=news.get('email'), password=news.get('password'))
    newo.save()
    return jsonify(newo.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """ Changes content in state
    """
    sobj = storage.get('User', user_id)
    if sobj is None:
        abort(404)
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    new_cont = request.get_json()
    for key, value in new_cont.items():
        setattr(sobj, key, value)
        sobj.save()
    return jsonify(sobj.to_dict()), 200
