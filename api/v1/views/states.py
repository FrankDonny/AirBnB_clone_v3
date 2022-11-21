#!/usr/bin/python3
"""This module handles default states requests"""
from flask import abort, request, jsonify
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """route function for GET method"""
    from models import storage
    return jsonify([obj.to_dict() for obj in storage.all("State").values()])


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """route function for POST method"""
    from models import storage
    new_state = request.get_json(silent=True)
    if type(new_state) != dict:
        abort(400, "Not a JSON")
    if "name" not in new_state.keys():
        abort(400, "Missing name")
    else:
        from models.state import State
        state = State(**new_state)
        storage.new(state)
        storage.save()
        return state.to_dict(), 201


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """route function for GET method"""
    from models import storage
    id_list = [key.split(".")[1] for key in storage.all("State").keys()]
    if state_id not in id_list:
        abort(404)
    state_obj = storage.get("State", state_id)
    return state_obj.to_dict()


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """route function for DELETE method"""
    from models import storage
    id_list = [key.split(".")[1] for key in storage.all("State").keys()]
    if state_id not in id_list:
        abort(404)
    value = storage.get("State", state_id)
    storage.delete(value)
    storage.save()
    storage.close()
    return {}, 200


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """route function for PUT method"""
    from models import storage
    id_list = [key.split(".")[1] for key in storage.all("State").keys()]
    if state_id not in id_list:
        abort(404)
    new_state = request.get_json(silent=True)
    if type(new_state) != dict:
        abort(400, "Not a JSON")
    state_obj = storage.get("State", state_id)
    key_list = ['id', 'created_at', 'updated_at']
    for ky, val in new_state.items():
        if ky in key_list:
            continue
        setattr(state_obj, ky, val)
    storage.save()
    return jsonify(state_obj.to_dict()), 200