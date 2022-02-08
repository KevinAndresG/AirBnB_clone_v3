#!/usr/bin/python3
'''
new view for State objects that handles all default RESTFul API actions
'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    '''
    use to_dict() to retrieve an object into a valid JSON
    '''
    list_dict = []
    object_id = storage.get("State", state_id)
    if object_id:
        for i in object_id.cities:
            list_dict.append(i.to_dict())
        return jsonify(list_dict)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(city_id):
    '''
    Retrieves a city object: GET /api/v1/cities/<city_id>
    '''
    city_obj = storage.get("City", city_id)
    if city_obj:
        return jsonify(city_obj.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    '''
    Deletes a city object: DELETE /api/v1/cities/<city_id>
    '''
    city_obj = storage.get('City', city_id)
    if city_obj:
        storage.delete(city_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    '''
    Creates a city: POST /api/v1/city
    '''
    cont = request.get_json()
    object_id = storage.get("State", state_id)
    if object_id:
        if type(cont) is dict:
            if "name" in cont.keys():
                new_state = City(state_id=object_id.id, **cont)
                storage.new(new_state)
                storage.save()
                return jsonify(new_state.to_dict()), 201
            abort(400, "Missing name")
        abort(400, "Not a JSON")
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_cities(city_id):
    '''
    Updates a city object: PUT /api/v1/states/<city_id>
    '''
    cont = request.get_json()
    remove_keys = ["state_id", "id", "created_at", "updated_at"]
    if type(cont) is dict:
        city_obj = storage.get('City', city_id)
        if city_obj:
            for key, value in cont.items():
                if key not in remove_keys:
                    setattr(city_obj, key, value)
                    storage.save()
                    return jsonify(city_obj.to_dict()), 200
        abort(404)
    abort(400, "Not a JSON")
