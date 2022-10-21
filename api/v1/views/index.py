#!/usr/bin/python3
'''creating an index route'''
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=['GET'])
def status():
    '''Returns the status fo the method'''
    if request.method == 'GET':
        return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def return_stats():
    '''returns a count of the instances of a class'''
    new_dict = {}
    for c in classes:
        count = storage.count(classes[c])
        new_dict[c] = count
        return jsonify(new_dict)
