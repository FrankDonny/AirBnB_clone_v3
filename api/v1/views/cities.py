#!/usr/bin/python3
"""This module handles default cities requests"""
<<<<<<< HEAD
from flask import abort, request, jsonify
=======
from flask import abort, request
>>>>>>> 0117a8b48a201e955532113ea7ad9b02cb440a49
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"],
                 strict_slashes=False)
def all_cities(state_id):
    """Return all cities depending on the state id"""
    from models import storage
    state_objects = storage.all("State")
    state_id_list = [k.split(".")[1] for k, v in state_objects.items()]
    city_objects = storage.all("City")
    if state_id not in state_id_list:
        abort(404)
    if request.method == "GET":
<<<<<<< HEAD
        return jsonify([value.to_dict() for value in city_objects.values()
                if value.state_id == state_id])
=======
        return [value.to_dict() for value in city_objects.values()
                if value.state_id == state_id], 200
>>>>>>> 0117a8b48a201e955532113ea7ad9b02cb440a49
    if request.method == "POST":
        new_city = request.get_json(silent=True)
        if not isinstance(new_city, dict):
            abort(400, "Not a JSON")
        elif "name" not in new_city.keys():
            abort(400, description="Missing name")
        else:
            from models.city import City
            new_city.update({"state_id": state_id})
            city = City(**new_city)
            storage.new(city)
            storage.save()
            return city.to_dict(), 201


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def city_object(city_id):
    """Returns a city object"""
    from models import storage
    city_objects = storage.all("City")
    cities_id_list = [k.split(".")[1] for k, v in city_objects.items()]
    if city_id not in cities_id_list:
        abort(404)
    if request.method == "GET":
        value = storage.get("City", city_id)
        return value.to_dict()
    if request.method == "DELETE":
        value = storage.get("City", city_id)
        storage.delete(value)
        storage.save()
        storage.close()
        return {}, 200
    if request.method == "PUT":
        value = storage.get("City", city_id)
        new_add = request.get_json(silent=True)
        if not isinstance(new_add, dict):
            abort(400, "Not a JSON")
        ignore = ["id", "created_at", "updated_at", "user_id", "city_id"]
        for key, val in new_add.items():
            if key in ignore:
                continue
            setattr(value, key, val)
        storage.save()
        return value.to_dict(), 200
