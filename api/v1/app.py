#!/usr/bin/python3
"""the flask server app"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def error_handler(e):
    """error handler method"""
    return jsonify({"error": "Not found"})


@app.teardown_appcontext
def teardown(exception):
    """method to handle remove of a session"""
    storage.close()


if __name__ == "__main__":
    ht = None
    pt = None
    if getenv("HBNB_API_HOST"):
        ht = getenv("HBNB_API_HOST")
    else:
        ht = "0.0.0.0"

    if getenv("HBNB_API_PORT"):
        pt = getenv("HBNB_API_PORT")
    else:
        pt = 5000
    app.run(host=ht, port=pt, threaded=True, debug=True)
