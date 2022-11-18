#!/usr/bin/python3
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/states/<state_id>", methods=["GET", "PUT", "DELETE"])
@app_views.route("/states/", methods=["GET", "POST"])
def get_state(state_id=None):
    """method to handle get request of state objects"""
    from models import storage
    objects = storage.all("State")
    obj_ls = []
    if request.method == "GET":
        id_list = []
        for k, v in objects.items():
            id_list.append(k.split(".")[1])
            if state_id:
                if k.split(".")[1] == state_id:
                    return jsonify(v.to_dict())
            else:
                obj_ls.append(v.to_dict())
        if state_id is None:
            return obj_ls
        abort(404)
    elif request.method == "POST":
        new_state = request.get_json(silent=True)
        try:
            if "name" not in new_state.keys():
                abort(400, description="Missing name")
            else:
                from models.state import State
                state = State(**new_state)
                storage.new(state)
                storage.save()
                return jsonify(state.to_dict()), 201
        except AttributeError:
            abort(400, description="Not a JSON")
    elif request.method == "PUT":
        new_state = request.get_json(silent=True)
        if new_state is None:
            abort(400, "Not a JSON")
        for k, v in objects.items():
            if k.split(".")[1] == state_id:
                key_list = ['id', 'created_at', 'updated_at']
                for ky, val in new_state.items():
                    if ky in key_list:
                        continue
                    setattr(v, ky, val)
                storage.save()
                return jsonify(v.to_dict())
            else:
                abort(404)
    else:
        id_list = []
        for key, value in objects.items():
            id_list.append(key.split(".")[1])
            if key.split(".")[1] == state_id:
                storage.delete(objects[key])
                storage.save()
                return {}
        if state_id not in id_list:
            abort(404)
