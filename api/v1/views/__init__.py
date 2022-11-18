#!/usr/bin/python3
"""init file contains the blueprint and default imports"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
# from api.v1.views.state import *
# from models.city import City
# from models.place import Place
# from models.review import Review
from api.v1.views.states import *
# from models.user import User
