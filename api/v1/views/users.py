#!/usr/bin/python3
'''
new view for amenities objects that handles all default RESTFul API actions
'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    '''
    use to_dict() to retrieve an object into a valid JSON
    '''
    list_dict = []
    all_user = storage.all("User")
    for i in all_user.values():
        list_dict.append(i.to_dict())
    return jsonify(list_dict)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def user_id(user_id):
    '''
    Retrieves a User object: GET /api/v1/users/<user_id>
    '''
    user = storage.get("User", user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    '''
    Deletes a user object: DELETE /api/v1/users/<user_id>
    '''
    id_user = storage.get("User", user_id)
    if id_user:
        storage.delete(id_user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''
    Creates a User: POST /api/v1/users
    '''
    cont = request.get_json()
    if type(cont) is dict:
        if "email" not in cont.keys():
            abort(400, "Missing email")
        elif "password" not in cont.keys():
            abort(400, "Missing password")
        else:
            new_user = User(**cont)
            storage.new(new_user)
            storage.save()
            return jsonify(new_user.to_dict()), 201
    abort(400, "Not a JSON")


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''
    Updates a user object: PUT /api/v1/users/<user_id>
    '''
    cont = request.get_json()
    remove_keys = ["email", "id", "created_at", "updated_at"]
    if type(cont) is dict:
        user_obj = storage.get('User', user_id)
        if user_obj:
            for key, value in cont.items():
                if key not in remove_keys:
                    setattr(user_obj, key, value)
                    storage.save()
                    return jsonify(user_obj.to_dict()), 200
        abort(404)
    abort(400, "Not a JSON")
