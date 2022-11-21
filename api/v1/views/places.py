#!/usr/bin/python3
"""This module handles default cities requests"""
from flask import abort, request, jsonify
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def places_list(city_id):
    pass


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"],
                 strict_slashes=False)
def place_list(city_id):
    """Return all place object depending on the city_id"""
    from models import storage
    city_objects = storage.all("City")
    place_objects = storage.all("Place")
    city_id_list = [key.split(".")[1] for key in city_objects.keys()]
    city_objects = storage.all("City")
    if city_id not in city_id_list:
        abort(404)
    if request.method == "GET":
        return [value.to_dict() for value in place_objects.values()
                if value.city_id == city_id], 200


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def create_object(city_id):
    from models import storage
    city_objects = storage.all("City")
    place_objects = storage.all("Place")
    city_id_list = [key.split(".")[1] for key in city_objects.keys()]
    if city_id not in city_id_list:
        abort(404)
    new_place = request.get_json(silent=True)
    if not isinstance(new_place, dict):
        abort(400, "Not a JSON")
    elif "user_id" not in new_place.keys():
        abort(400, description="Missing user_id")
    elif new_place["user_id"] not in [key.split(".")[1] for key in storage.all("User").keys()]:
        abort(404)
    elif "name" not in new_place.keys():
        abort(400, description="Missing name")
    else:
        from models.place import Place
        new_place.update({"city_id": city_id})
        place = Place(**new_place)
        storage.new(place)
        storage.save()
        return place.to_dict(), 201


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_object(place_id):
    pass


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_object(place_id):
    pass


@app_views.route("/cities/<city_id>/places", methods=["PUT"], strict_slashes=False)
def update_object(place_id):
    pass



# def place_list(city_id):
#     """Return all place object depending on the city_id"""
#     from models import storage
#     city_objects = storage.all("City")
#     place_objects = storage.all("Place")
#     city_id_list = [key.split(".")[1] for key in city_objects.keys()]
#     city_objects = storage.all("City")
#     if city_id not in city_id_list:
#         abort(404)
#     if request.method == "GET":
#         return [value.to_dict() for value in place_objects.values()
#                 if value.city_id == city_id], 200
#     if request.method == "POST":
#         new_place = request.get_json(silent=True)
#         if not isinstance(new_place, dict):
#             abort(400, "Not a JSON")
#         elif "user_id" not in new_place.keys():
#             abort(400, description="Missing user_id")
#         elif new_place["user_id"] not in [key.split(".")[1]
#                                           for key in storage.all("User").keys()]:
#             abort(404)
#         elif "name" not in new_place.keys():
#             abort(400, description="Missing name")
#         else:
#             from models.place import Place
#             new_place.update({"city_id": city_id})
#             place = Place(**new_place)
#             storage.new(place)
#             storage.save()
#             return place.to_dict(), 201
# #
# #
# @app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"],
#                  strict_slashes=False)
# def place_object(place_id):
#     """Returns a place object"""
#     from models import storage
#     place_objects = storage.all("Place")
#     place_id_list = [key.split(".")[1] for key in place_objects.keys()]
#     if place_id not in place_id_list:
#         abort(404)
#     if request.method == "GET":
#         value = storage.get("Place", place_id)
#         return value.to_dict()
#     if request.method == "DELETE":
#         value = storage.get("Place", place_id)
#         storage.delete(value)
#         storage.save()
#         storage.close()
#         return {}, 200
#     if request.method == "PUT":
#         value = storage.get("Place", place_id)
#         new_add = request.get_json(silent=True)
#         if not isinstance(new_add, dict):
#             abort(400, "Not a JSON")
#         ignore = ["id", "created_at", "updated_at"]
#         for key, val in new_add.items():
#             if key in ignore:
#                 continue
#             setattr(value, key, val)
#         storage.save()
#         return value.to_dict(), 200
    if request.method == "POST":
        new_place = request.get_json(silent=True)
        if not isinstance(new_place, dict):
            abort(400, "Not a JSON")
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
            return place.to_dict(), 201
#
#
@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def place_object(place_id):
    """Returns a place object"""
    from models import storage
    place_objects = storage.all("Place")
    place_id_list = [key.split(".")[1] for key in place_objects.keys()]
    if place_id not in place_id_list:
        abort(404)
    if request.method == "GET":
        value = storage.get("Place", place_id)
        return value.to_dict()
    if request.method == "DELETE":
        value = storage.get("Place", place_id)
        storage.delete(value)
        storage.save()
        storage.close()
        return {}, 200
    if request.method == "PUT":
        value = storage.get("Place", place_id)
        new_add = request.get_json(silent=True)
        if not isinstance(new_add, dict):
            abort(400, "Not a JSON")
        ignore = ["id", "created_at", "updated_at"]
        for key, val in new_add.items():
            if key in ignore:
                continue
            setattr(value, key, val)
        storage.save()
        return value.to_dict(), 200
