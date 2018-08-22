#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models import Amenity
from models import City
from models import Place
from models import Review
from models import State
from models import User
from models import base_model


@app_views.route('/states', strict_slashes=False)
def get_states():
    """ returns state info
    """
    emli = []
    stateinfo = storage.all('State')
    for key, value in stateinfo.items():
        emli.append(value.to_dict())
    return jsonify(emli)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """ Returns info for <state_id>
    """
    try:
        vari = storage.get('State', state_id)
        return jsonify(vari.to_dict())
    except:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_id(state_id):
    """ Returns info for <state_id>
    """
    try:
        var_all = storage.all('State')
        var_id = 'State.' + state_id
        var_obj = var_all.get(var_id)
        var_obj.delete()
        storage.save()
        return jsonify({}), 200
    except:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Adds a new state to State
    """
    try:
        if request.json:
            if 'name' not in request.json:
                return jsonify({'error': 'Missing name'}), 400
            news = request.get_json().get('name')
            newo = State(name=news)
            newo.save()
            return jsonify(newo.to_dict()), 201
        else:
            return jsonify({'error': 'Not a JSON'}), 400
    except:
        abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Changes content in state
    """
    try:
        sobj = storage.get('State', state_id)
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
