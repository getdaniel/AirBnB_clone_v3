#!/usr/bin/python3
""" State APIRest
"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def list_dict():
    """ list of an objetc in a dict form
    """
    lista = []
    dic = storage.all('State')
    for elem in dic:
        lista.append(dic[elem].to_dict())
    return (jsonify(lista))


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def state_id(state_id):
    """ realize the specific action depending on method
    """
    lista = []
    dic = storage.all('State')
    for elem in dic:
        var = dic[elem].to_dict()
        if var["id"] == state_id:
            if request.method == 'GET':
                return (jsonify(var))
            elif request.method == 'DELETE':
                aux = {}
                dic[elem].delete()
                storage.save()
                return (jsonify(aux))
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def add_item():
    """ add a new item
    """
    if not request.json:
        return jsonify("Not a JSON"), 400
    else:
        content = request.get_json()
        if "name" not in content.keys():
            return jsonify("Missing name"), 400
        else:
            new_state = State(**content)
            new_state.save()
            return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_item(state_id):
    """ update item
    """
    dic = storage.all("State")
    for key in dic:
        if dic[key].id == state_id:
            if not request.json:
                return jsonify("Not a JSON"), 400
            else:
                forbidden = ["id", "update_at", "created_at"]
                content = request.get_json()
                for k in content:
                    if k not in forbidden:
                        setattr(dic[key], k, content[k])
                dic[key].save()
                return(jsonify(dic[key].to_dict()))
    abort(404)
