#!/usr/bin/python3
"""This module handles default users requests"""
from flask import abort, request
from api.v1.views import app_views


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def users():
    """route function for GET and POST"""
    from models import storage
    if request.method == "GET":
        return [value.to_dict() for value in storage.all("User").values()]
    if request.method == "POST":
        new_user = request.get_json(silent=True)
        if type(new_user) != dict:
            abort(400, "Not a JSON")
        if "email" not in new_user.keys():
            abort(400, "Missing email")
        elif "password" not in new_user.keys():
            abort(400, "Missing password")
        else:
            from models.user import User
            user = User(**new_user)
            storage.new(user)
            storage.save()
            return user.to_dict(), 201


@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def users_with_id(user_id):
    """route function for GET, DELETE and PUT"""
    from models import storage
    user_ids = [key.split(".")[1] for key in storage.all("User").keys()]
    if user_id not in user_ids:
        abort(404)
    user_object = storage.get("User", user_id)
    if request.method == "GET":
        return user_object.to_dict()
    if request.method == "DELETE":
        storage.delete(user_object)
        storage.save()
        storage.close()
        return {}, 200
    if request.method == "PUT":
        value = storage.get("User", user_id)
        new_addons = request.get_json(silent=True)
        if type(new_addons) != dict:
            abort(400, "Not a JSON")
        key_list = ['id', 'created_at', 'updated_at']
        for ky, val in new_addons.items():
            if ky in key_list:
                continue
            setattr(value, ky, val)
        storage.save()
        return value.to_dict(), 200
