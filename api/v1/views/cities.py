#!/usr/bin/python3
"""This module handles default cities requests"""
from flask import abort, request
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def all_cities(state_id=None):
    """Return all cities depending on the state id"""
    from models import storage
    state_objects = storage.all("State")
    state_id_list = [k.split(".")[1] for k, v in state_objects.items()]
    city_objects = storage.all("City")
    if state_id not in state_id_list:
        abort(404)
    if request.method == "GET":
        all__cities = []
        for key, value in city_objects.items():
            if value.state_id == state_id:
                all__cities.append(value.to_dict())
        return all__cities
    else:
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


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def city_object(city_id):
    """Returns a city object"""
    from models import storage
    city_objects = storage.all("City")
    cities_id_list = [k.split(".")[1] for k, v in city_objects.items()]
    if city_id not in cities_id_list:
        abort(404)
    for key, value in city_objects.items():
        if value.id == city_id:
            if request.method == "DELETE":
                storage.delete(value)
                storage.save()
                return {}
            elif request.method == "GET":
                return value.to_dict()
            else:
                new_city = request.get_json(silent=True)
                if not isinstance(new_city, dict):
                    abort(400, "Not a JSON")
                else:
                    id_list = []
                    for k, v in city_objects.items():
                        id_list.append(k.split(".")[1])
                        if k.split(".")[1] == city_id:
                            key_list = ['id', 'created_at', 'updated_at']
                            for ky, val in new_city.items():
                                if ky in key_list:
                                    continue
                                setattr(v, ky, val)
                            storage.save()
                            return v.to_dict()