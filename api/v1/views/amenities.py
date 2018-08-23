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


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """ returns state info
    """
    emli = []
    stateinfo = storage.all('Amenity')
    for key, value in stateinfo.items():
        citi = value.to_dict()
        emli.append(citi)
    return jsonify(emli)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a City object
    """
    if storage.get('Amenity', amenity_id) is None:
        abort(404)
    vari = storage.get('Amenity', amenity_id)
    return jsonify(vari.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Returns info for <state_id>
    """
    if storage.get('Amenity', amenity_id) is None:
        abort(404)
    var_all = storage.all('Amenity')
    var_id = 'Amenity.' + amenity_id
    var_obj = var_all.get(var_id)
    var_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """ Adds a new state to State
    """
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.json:
        return jsonify({'error': 'Missing name'}), 400
    news = request.get_json().get('name')
    newo = Amenity(name=news)
    newo.save()
    return jsonify(newo.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Changes content in state
    """
    if storage.get('Amenity', amenity_id) is None:
        abort(404)
    sobj = storage.get('Amenity', amenity_id)
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    new_cont = request.get_json()
    tmp = {'id', 'created_at', 'updated_at'}
    for key, value in new_cont.items():
        if key not in tmp:
            setattr(sobj, key, value)
            sobj.save()
    return jsonify(sobj.to_dict()), 200
