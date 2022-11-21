#!/usr/bin/python3
"""This module handles default cities requests"""
from flask import abort, request, jsonify
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_list(city_id):
    """Return all place object depending on the city_id"""
    from models import storage
    city_id_list = [key.split(".")[1] for key in storage.all("City").keys()]
    if city_id not in city_id_list:
        abort(404)
    return jsonify([value.to_dict() for value in storage.all("Place").values()
                   if value.city_id == city_id]), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_object(city_id):
    """creates new place instance"""
    from models import storage
    if city_id not in [key.split(".")[1]
                       for key in storage.all("City").keys()]:
        abort(404)
    new_place = request.get_json(silent=True)
    if not isinstance(new_place, dict):
        abort(400, description="Not a JSON")
    elif "user_id" not in new_place.keys():
        abort(400, description="Missing user_id")
    elif new_place["user_id"] not in [key.split(".")[1]
                                      for key in storage.all("User").keys()]:
        abort(404)
    elif "name" not in new_place.keys():
        abort(400, description="Missing name")
    else:
        from models.place import Place
        new_place.update({"city_id": city_id})
        place = Place(**new_place)
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_object(place_id):
    """Returns a place object"""
    from models import storage
    if place_id not in [key.split(".")[1]
                        for key in storage.all("Place").keys()]:
        abort(404)
    obj = storage.get("Place", place_id)
    return jsonify(obj.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_object(place_id):
    """delete a place object"""
    from models import storage
    if place_id not in [key.split(".")[1]
                        for key in storage.all("Place").keys()]:
        abort(404)
    place = storage.get("Place", place_id)
    storage.delete(place)
    storage.save()
    storage.close()
    return {}, 200


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_object(place_id):
    """update a place object"""
    from models import storage
    if place_id not in [key.split(".")[1]
                        for key in storage.all("Place").keys()]:
        abort(404)
    place = storage.get("Place", place_id)
    new_add = request.get_json(silent=True)
    if not isinstance(new_add, dict):
        abort(400, "Not a JSON")
    ignore = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for key, val in new_add.items():
        if key in ignore:
            continue
        setattr(place, key, val)
    storage.save()
    return place.to_dict(), 200
