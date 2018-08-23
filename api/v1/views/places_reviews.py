#!/usr/bin/python3
"""Place objects that handles all default RestFul API actions"""


from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models import Amenity
from models import City
from models import Place
from models import Review
from models import State
from models import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ returns state info
    """
    if storage.get('Place', place_id) is None:
        abort(404)
    emli = []
    stateinfo = storage.all('Review')
    for key, value in stateinfo.items():
        revw = value.to_dict()
        if revw.get('place_id') == place_id:
            emli.append(revw)
    return jsonify(emli)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieves a  Place object
    """
    vari = storage.get('Review', review_id)
    if vari is None:
        abort(404)
    return jsonify(vari.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete place
    """
    vari = storage.get('Review', review_id)
    if vari is None:
        abort(404)
    vari.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ Adds a new place
    """
    citi = storage.get('Place', place_id)
    if citi is None:
        abort(404)
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in request.json:
        return jsonify({'error': 'Missing user_id'}), 400
    usr_id = request.get_json().get('user_id')
    if storage.get('User', usr_id) is None:
        abort(404)
    if 'text' not in request.json:
        return jsonify({'error': 'Missing text'}), 400
    txt = request.get_json().get('text')
    newo = Review(text=txt, user_id=usr_id, place_id=place_id)
    newo.save()
    return jsonify(newo.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """ Put some content to place
    """
    sobj = storage.get('Review', review_id)
    if sobj is None:
        abort(404)
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    new_cont = request.get_json()
    for key, value in new_cont.items():
        setattr(sobj, key, value)
        sobj.save()
    return jsonify(sobj.to_dict()), 200
