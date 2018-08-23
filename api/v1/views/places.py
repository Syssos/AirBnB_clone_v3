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


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ returns state info
    """
    if storage.get('City', city_id) is None:
        abort(404)
    emli = []
    stateinfo = storage.all('Place')
    for key, value in stateinfo.items():
        plac = value.to_dict()
        if plac.get('city_id') == city_id:
            emli.append(plac)
    return jsonify(emli)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a City object
    """
    vari = storage.get('Place', place_id)
    if vari is None:
        abort(404)
    return jsonify(vari.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Returns info for <state_id>
    """
    vari = storage.get('Place', place_id)
    if vari is None:
        abort(404)
    var_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Adds a new state to State
    """
    citi = storage.get('City', city_id)
    if citi is None:
        abort(404)
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in request.json:
        return jsonify({'error': 'Missing user_id'}), 400
    usr_id = request.get_json().get('user_id')
    if storage.get('User', usr_id) is None:
        abort(404)
    if 'name' not in request.json:
        return jsonify({'error': 'Missing name'}), 400
    news = request.get_json().get('name')
    newo = Place(name=news, user_id=usr_id, city_id=city_id)
    newo.save()
    return jsonify(newo.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ Changes content in state
    """
    sobj = storage.get('Place', place_id)
    if sobj is None:
        abort(404)
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    new_cont = request.get_json()
    tmp = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in new_cont.items():
        if key not in tmp:
            setattr(sobj, key, value)
            sobj.save()
    return jsonify(sobj.to_dict()), 200
