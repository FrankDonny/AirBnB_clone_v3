#!/usr/bin/python3
"""This module handles default lining with amenities
and places object requests"""
from flask import abort, jsonify
from api.v1.views import app_views
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_places_amenities(place_id):
    """get all amenities based on place id"""
    from models import storage
    place_ids = [key.split(".")[1] for key in storage.all("Place").keys()]
    if place_id not in place_ids:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_obj = storage.get("Place", place_id)
        return jsonify(place_obj.amenities)
    else:
        amenities = storage.all("Amenity")
        place_obj = storage.get("Place", place_id)
        all_amenities = [amenity for amenity in amenities
                         if amenity.id in place_obj.amenity_ids]
        return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenityObj(place_id, amenity_id):
    """delete an amenity object"""
    from models import storage
    place_ids = [key.split(".")[1] for key in storage.all("Place").keys()]
    if place_id not in place_ids:
        abort(404)
    if amenity_id not in [key.split(".")[1]
                          for key in storage.all("Amenity").keys()]:
        abort(404)
    place_obj = storage.get("Place", place_id)
    amenity_object = storage.get("Amenity", amenity_id)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity_object not in place_obj.amenities:
            abort(404)
        storage.delete(amenity_object)
        storage.save()
        storage.close()
        return {}, 200
    else:
        if amenity_id not in place_obj.amenity_ids:
            abort(404)
        storage.delete(amenity_object)
        place_obj.amenity_ids.pop(place_obj.amenity_ids.index(amenity_id))
        storage.save()
        storage.close()
        return {}, 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def create_amenities(place_id, amenity_id):
    """append new amenity to a place"""
    from models import storage
    place_ids = [key.split(".")[1] for key in storage.all("Place").keys()]
    if place_id not in place_ids:
        abort(404)
    if amenity_id not in [key.split(".")[1]
                          for key in storage.all("Amenity").keys()]:
        abort(404)
    place_obj = storage.get("Place", place_id)
    amenity_object = storage.get("Amenity", amenity_id)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity_object in place_obj.amenities:
            return jsonify(amenity_object.to_dict()), 200
        place_obj.amenities.append(amenity_object)
        storage.save()
        return jsonify(amenity_object.to_dict()), 201
    else:
        if amenity_object.id in place_obj.amenity_ids:
            return amenity_object.to_dict(), 200
        place_obj.amenity_ids.append(amenity_object.id)
        storage.save()
        return jsonify(amenity_object.to_dict()), 201
