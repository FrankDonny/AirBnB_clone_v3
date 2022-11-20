#!/usr/bin/python3
"""This module handles default states requests"""
from flask import abort, request
from api.v1.views import app_views


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def states_obj():
    """route function for GET and POST"""
    from models import storage
    objects = storage.all("State")
    if request.method == "POST":
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
    if request.method == "GET":
        return [value.to_dict() for value in objects.values()]


@app_views.route("/states/<state_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def states_with_id(state_id):
    """route function for GET, PUT and DELETE"""
    from models import storage
    objects = storage.all("State")
    id_list = [key.split(".")[1] for key in objects.keys()]
    if state_id not in id_list:
        abort(404)
    if request.method == "GET":
        for key, value in objects.items():
            if key.split(".")[1] == state_id:
                return value.to_dict()
    if request.method == "DELETE":
        value = storage.get("State", state_id)
        storage.delete(value)
        storage.save()
        storage.close()
        return {}, 200
    if request.method == "PUT":
        value = storage.get("State", state_id)
        new_state = request.get_json(silent=True)
        if type(new_state) != dict:
            abort(400, "Not a JSON")
        key_list = ['id', 'created_at', 'updated_at']
        for ky, val in new_state.items():
            if ky in key_list:
                continue
            setattr(value, ky, val)
        storage.save()
        return value.to_dict(), 200
