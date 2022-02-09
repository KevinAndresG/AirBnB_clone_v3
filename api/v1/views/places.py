#!/usr/bin/python3
'''
new view for Place objects that handles all default RESTFul API actions
'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_place(city_id):
    '''
    use to_dict() to retrieve an object into a valid JSON
    '''
    list_dict = []
    object_id = storage.get("City", city_id)
    if object_id:
        for i in object_id.places:
            list_dict.append(i.to_dict())
        return jsonify(list_dict)
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id):
    '''
    Retrieves a place object: GET /api/v1/places/<place_id>
    '''
    place_obj = storage.get("Place", place_id)
    if place_obj:
        return jsonify(place_obj.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''
    Deletes a city object: DELETE /api/v1/places/<place_id>>
    '''
    place_obj = storage.get('Place', place_id)
    if place_obj:
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    '''
    Creates a city: POST /api/v1/city
    '''
    cont = request.get_json()
    city_obj = storage.get("City", city_id)
    user_obj = storage.get("User", cont['user_id'])
    if type(cont) is not dict:
        abort(400, "Not a JSON")
    if "name" not in cont.keys():
        abort(400, "Missing name")
    if "user_id" not in cont.keys():
        abort(400, "Missing user_id")
    if not city_obj:
        abort(404)
    if user_obj is None:
        abort(404)

    cont['city_id'] = city_obj.id
    cont['user_id'] = user_obj.id
    new_place = Place(**cont)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''
    Updates a place object: PUT /api/v1/places/<place_id>
    '''
    cont = request.get_json()
    remove_keys = ["user_id", "id", "created_at", "updated_at"]
    if type(cont) is dict:
        place_obj = storage.get('Place', place_id)
        if place_obj:
            for key, value in cont.items():
                if key not in remove_keys:
                    setattr(place_obj, key, value)
                    storage.save()
                    return jsonify(place_obj.to_dict()), 200
        abort(404)
    abort(400, "Not a JSON")
