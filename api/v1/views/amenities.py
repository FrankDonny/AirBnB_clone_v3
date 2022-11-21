#!/usr/bin/python3
"""This module handles default amenities requests"""
from flask import abort, request, jsonify
from api.v1.views import app_views


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """route function for GET"""
    from models import storage
    return [obj.to_dict() for obj in storage.all("Amenity").values()]


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """route function for GET and POST"""
    from models import storage
    new_amenity = request.get_json(silent=True)
    if not isinstance(new_amenity, dict):
        abort(400, "Not a JSON")
    elif "name" not in new_amenity.keys():
        abort(400, "Missing name")
    else:
        from models.amenity import Amenity
        amenity = Amenity(**new_amenity)
        storage.new(amenity)
        storage.save()
        return amenity.to_dict(), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """route function for GET with id"""
    from models import storage
    amenity_ids = [key.split(".")[1] for key in storage.all("Amenity").keys()]
    if amenity_id not in amenity_ids:
        abort(404)
    amenity_obj = storage.get("Amenity", amenity_id)
    return amenity_obj.to_dict()


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """route function for DELETE"""
    from models import storage
    amenity_ids = [key.split(".")[1] for key in storage.all("Amenity").keys()]
    if amenity_id not in amenity_ids:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    storage.delete(amenity)
    storage.save()
    storage.close()
    return {}, 200


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """route function for PUT"""
    from models import storage
    amenity_ids = [key.split(".")[1] for key in storage.all("Amenity").keys()]
    if amenity_id not in amenity_ids:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    new_add = request.get_json(silent=True)
    if not isinstance(new_add, dict):
        abort(400, "Not a JSON")
    ignore = ["id", "created_at", "updated_at"]
    for key, value in new_add.items():
        if key in ignore:
            continue
        setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 202
