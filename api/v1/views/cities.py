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


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """ returns state info
    """
    emli = []
    stateinfo = storage.all('City')
    for key, value in stateinfo.items():
        citi = value.to_dict()
        if citi.get('state_id') == state_id:
            emli.append(citi)
    if len(emli) > 0:
        return jsonify(emli)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """ Retrieves a City object
    """
    try:
        vari = storage.get('City', city_id)
        return jsonify(vari.to_dict())
    except BaseException:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Returns info for <state_id>
    """
    try:
        var_all = storage.all('City')
        var_id = 'City.' + city_id
        var_obj = var_all.get(var_id)
        var_obj.delete()
        storage.save()
        return jsonify({}), 200
    except BaseException:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ Adds a new state to State
    """
    try:
        if request.json:
            if 'name' not in request.json:
                return jsonify({'error': 'Missing name'}), 400
            news = request.get_json().get('name')
            state = storage.get('State', state_id)
            if state is None:
                abort(404)
            newo = City(name=news, state_id=state_id)
            newo.save()
            return jsonify(newo.to_dict()), 201
        return jsonify({'error': 'Not a JSON'}), 400
    except BaseException:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ Changes content in state
    """
    try:
        sobj = storage.get('City', city_id)
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400
        elif sobj is None:
            abort(404)

        new_cont = request.get_json()
        tmp = {'id', 'created_at', 'updated_at'}
        for key, value in new_cont.items():
            if key not in tmp:
                setattr(sobj, key, value)
        sobj.save()
        return jsonify(sobj.to_dict()), 200

    except Exception:
        abort(404)
