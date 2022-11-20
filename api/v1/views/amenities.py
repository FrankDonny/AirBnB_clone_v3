#!/usr/bin/python3
"""This module handles default amenities requests"""
from flask import abort, request
from api.v1.views import app_views


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
def amenity_object():
    """route function for GET and POST"""
    from models import storage
    if request.method == "GET":
        return [value.to_dict() for value in storage.all("Amenity").values()]
    if request.method == "POST":
        new_amenity = request.get_json(silent=True)
        if not isinstance(new_amenity, dict):
            abort(400, "Not a JSON")
        if "name" not in new_amenity.keys():
            abort(400, "Missing name")
        from models.amenity import Amenity
        amenity_ = Amenity(**new_amenity)
        storage.new(amenity_)
        storage.save()
        return amenity_.to_dict(), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def amenities_with_id(amenity_id):
    """route function for GET, DELETE and PUT"""
    from models import storage
    amenity_ids = [key.split(".")[1] for key in storage.all("Amenity").keys()]
    if amenity_id not in amenity_ids:
        abort(404)
    amenity_obj = storage.get("Amenity", amenity_id)
    if request.method == "GET":
        return amenity_obj.to_dict()
    if request.method == "DELETE":
        storage.delete(amenity_obj)
        storage.save()
        storage.close()
        return {}, 200
    if request.method == "PUT":
        updated_obj = request.get_json(silent=True)
        if not isinstance(value, dict):
            abort(400, "Not a JSON")
        ignore = ["id", "created_at", "updated_at"]
        for key, value in updated_obj.items():
            if key in ignore:
                continue
            setattr(amenity_obj, key, value)
        return amenity_obj, 202
