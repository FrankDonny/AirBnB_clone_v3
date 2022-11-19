#!/usr/bin/python3
"""This module handles default cities requests"""
from flask import abort, request
from api.v1.views import app_views


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"])
@app_views.route("/amenities", methods=["GET", "POST"])
def all_amenities(amenity_id=None):
    from models import storage
    amenity_objects = storage.all("Amenity")
    if amenity_id is None:
        if request.method == "POST":
            new_amenity = request.get_json(silent=True)
            if not isinstance(new_amenity, dict):
                abort(400, "Not a JSON")
            elif "name" not in new_amenity.keys():
                abort(400, description="Missing name")
            else:
                from models.amenity import Amenity
                amenity = Amenity(**new_amenity)
                storage.new(amenity)
                storage.save()
                return amenity.to_dict(), 201
        else:
            return [value.to_dict() for value in amenity_objects.values()]
    amenity_id_list = [key.split(".")[1] for key in amenity_objects.keys()]
    if amenity_id not in amenity_id_list:
        abort(404)
    else:
        for key, value in amenity_objects.items():
            if key.split(".")[1] == amenity_id:
                if request.method == "DELETE":
                    storage.delete(value)
                    storage.save()
                    return {}
                elif request.method == "PUT":
                    new_amenity = request.get_json(silent=True)
                    if not isinstance(new_amenity, dict):
                        abort(400, "Not a JSON")
                    else:
                        id_list = []
                        for k, v in amenity_objects.items():
                            id_list.append(k.split(".")[1])
                            if k.split(".")[1] == amenity_id:
                                key_list = ['id', 'created_at', 'updated_at']
                                for ky, val in new_amenity.items():
                                    if ky in key_list:
                                        continue
                                    setattr(v, ky, val)
                                storage.save()
                                return v.to_dict()
                return value.to_dict()
