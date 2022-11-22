#!/usr/bin/python3
"""This module handles default states requests"""
from flask import abort, request, jsonify
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves all reviews based on place_id"""
    from models import storage
    if place_id not in [key.split(".")[1]
                        for key in storage.all("Place").keys()]:
        abort(404)
    return jsonify([obj.to_dict() for obj in storage.all("Review").values()
                    if obj.place_id == place_id])


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """creates a new review object"""
    from models import storage
    from models.review import Review
    if place_id not in [key.split(".")[1]
                        for key in storage.all("Place").keys()]:
        abort(404)
    new_review = request.get_json(silent=True)
    if not isinstance(new_review, dict):
        abort(400, description="Not a JSON")
    if "user_id" not in new_review.keys():
        abort(400, description="Missing user_id")
    if new_review["user_id"] not in [key.split(".")[1]
                                     for key in storage.all("User").keys()]:
        abort(404)
    if "text" not in new_review.keys():
        abort(400, description="Missing text")
    new_review.update({"place_id": place_id})
    review = Review(**new_review)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """retrieves a review object"""
    from models import storage
    if review_id not in [key.split(".")[1]
                         for key in storage.all("Review").keys()]:
        abort(404)
    review = storage.get("Review", review_id)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """delete a review instance"""
    from models import storage
    if review_id not in [key.split(".")[1]
                         for key in storage.all("Review").keys()]:
        abort(404)
    review = storage.get("Review", review_id)
    storage.delete(review)
    storage.save()
    storage.close()
    return {}, 200


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """updates a review instance"""
    from models import storage
    if review_id not in [key.split(".")[1]
                         for key in storage.all("Review").keys()]:
        abort(404)
    review = request.get_json(silent=True)
    if not isinstance(review, dict):
        abort(400, description="Not a JSON")
    review_obj = storage.get("Review", review_id)
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in review.items():
        if key in ignore:
            continue
        setattr(review_obj, key, value)
    storage.save()
    return jsonify(review_obj.to_dict()), 200
