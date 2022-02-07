#!/usr/bin/python3
'''
new view for State objects that handles all default RESTFul API actions
'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    '''
    use to_dict() to retrieve an object into a valid JSON
    '''
    list_dict = []
    all_states = storage.all("State")
    for i in all_states.values():
        list_dict.append(i.to_dict())
    return jsonify(list_dict)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_id(state_id):
    '''
    Retrieves a State object: GET /api/v1/states/<state_id>
    '''
    id_state = storage.get('State', state_id)
    if id_state:
        return jsonify(id_state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    '''
    Deletes a State object: DELETE /api/v1/states/<state_id>
    '''
    id_state = storage.get('State', state_id)
    if id_state:
        storage.delete(id_state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''
    Creates a State: POST /api/v1/states
    '''
    cont = request.get_json()
    if type(cont) is dict:
        if "name" in cont.keys():
            new_state = State(**cont)
            storage.new(new_state)
            storage.save()
            return jsonify(new_state.to_dict()), 201
        abort(400, "Missing name")
    abort(400, "Not a JSON")


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_states(state_id):
    '''
    Updates a State object: PUT /api/v1/states/<state_id>
    '''
    cont = request.get_json()
    if type(cont) is dict:
        name = cont['name']
        state_obj = storage.get('State', state_id)
        if state_obj:
            state_obj.name = name
            storage.save()
            return jsonify(state_obj.to_dict()), 200
        abort(404)
    abort(400, "Not a JSON")
