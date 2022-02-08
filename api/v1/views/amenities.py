#!/usr/bin/python3
'''
new view for amenities objects that handles all default RESTFul API actions
'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    '''
    use to_dict() to retrieve an object into a valid JSON
    '''
    list_dict = []
    all_states = storage.all("Amenity")
    for i in all_states.values():
        list_dict.append(i.to_dict())
    return jsonify(list_dict)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenities_id(amenity_id):
    '''
    Retrieves a State object: GET /api/v1/amenities/<amenity_id>
    '''
    id_amenity = storage.get("Amenity", amenity_id)
    if id_amenity:
        return jsonify(id_amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_anmenity(amenity_id):
    '''
    Deletes a State object: DELETE /api/v1/amenities/<amenity_id>
    '''
    id_amenity = storage.get("Amenity", amenity_id)
    if id_amenity:
        storage.delete(id_amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''
    Creates a State: POST /api/v1/amenities
    '''
    cont = request.get_json()
    if type(cont) is dict:
        if "name" in cont.keys():
            new_amenity = Amenity(**cont)
            storage.new(new_amenity)
            storage.save()
            return jsonify(new_amenity.to_dict()), 201
        abort(400, "Missing name")
    abort(400, "Not a JSON")


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''
    Updates a State object: PUT /api/v1/amenities/<amenity_id>
    '''
    cont = request.get_json()
    remove_keys = ["id", "created_at", "updated_at"]
    if type(cont) is dict:
        amenity_obj = storage.get("Amenity", amenity_id)
        if amenity_obj:
            for key, value in cont.items():
                if key not in remove_keys:
                    setattr(amenity_obj, key, value)
                    storage.save()
                    return jsonify(amenity_obj.to_dict()), 200
        abort(404)
    abort(400, "Not a JSON")
