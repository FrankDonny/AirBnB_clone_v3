#!/usr/bin/python3
"""This module handles default cities requests"""
from flask import abort, request, jsonify
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """Return all cities depending on the state id"""
    from models import storage
    if state_id not in [key.split(".")[1]
                        for key in storage.all("State").keys()]:
        abort(404)
    return jsonify([obj.to_dict() for obj in storage.all("City").values()
                   if obj.state_id == state_id]), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """create a new city instance"""
    from models import storage
    if state_id not in [key.split(".")[1]
                        for key in storage.all("State").keys()]:
        abort(404)
    new_city = request.get_json(silent=True)
    if not isinstance(new_city, dict):
        abort(400, description="Not a JSON")
    elif "name" not in new_city.keys():
        abort(400, description="Missing name")
    else:
        from models.city import City
        new_city.update({"state_id": state_id})
        city = City(**new_city)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """Returns a city object"""
    from models import storage
    if city_id not in [k.split(".")[1]
                       for k, v in storage.all("City").items()]:
        abort(404)
    obj = storage.get("City", city_id)
    return jsonify(obj.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes a city instance"""
    from models import storage
    if city_id not in [key.split(".")[1]
                       for key in storage.all("City").keys()]:
        abort(404)
    city = storage.get("City", city_id)
    storage.delete(city)
    storage.save()
    storage.close()
    return {}, 200


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """update a city instance"""
    from models import storage
    if city_id not in [key.split(".")[1]
                       for key in storage.all("City").keys()]:
        abort(404)
    city = storage.get("City", city_id)
    new_add = request.get_json(silent=True)
    if not isinstance(new_add, dict):
        abort(400, "Not a JSON")
    ignore = ["id", "created_at", "updated_at", "state_id"]
    for key, val in new_add.items():
        if key in ignore:
            continue
        setattr(city, key, val)
    storage.save()
    return jsonify(city.to_dict()), 200
