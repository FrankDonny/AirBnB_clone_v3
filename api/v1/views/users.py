#!/usr/bin/python3
"""This module handles default users requests"""
from flask import abort, request, jsonify
from api.v1.views import app_views


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """get list of all users"""
    from models import storage
    return jsonify([obj.to_dict() for obj in storage.all("User").values()])


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """creates a new user method"""
    from models import storage
    new_user = request.get_json(silent=True)
    if not isinstance(new_user, dict):
        abort(400, description="Not a JSON")
    if "email" not in new_user.keys():
        abort(400, description="Missing email")
    elif "password" not in new_user.keys():
        abort(400, description="Missing password")
    else:
        from models.user import User
        user = User(**new_user)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """get a user object"""
    from models import storage
    if user_id not in [key.split(".")[1]
                       for key in storage.all("User").keys()]:
        abort(404)
    user_object = storage.get("User", user_id)
    return jsonify(user_object.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """delete a user"""
    from models import storage
    if user_id not in [key.split(".")[1]
                       for key in storage.all("User").keys()]:
        abort(404)
    user_object = storage.get("User", user_id)
    storage.delete(user_object)
    storage.save()
    storage.close()
    return {}, 200


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """update a user"""
    from models import storage
    if user_id not in [key.split(".")[1]
                       for key in storage.all("User").keys()]:
        abort(404)
    value = storage.get("User", user_id)
    new_addons = request.get_json(silent=True)
    if not isinstance(new_addons, dict):
        abort(400, "Not a JSON")
    key_list = ['id', 'created_at', 'updated_at', 'email']
    for ky, val in new_addons.items():
        if ky in key_list:
            continue
        setattr(value, ky, val)
    storage.save()
    return jsonify(value.to_dict()), 200
