#!/usr/bin/python3
"""This module contains the index route of the blueprint app_views"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def status():
    """returns OK status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stat():
    """method to retrieve number of objects by type"""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
