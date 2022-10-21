#!/usr/bin/python3
'''creating an index route'''
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def status():
    '''Returns the status fo the method'''
    if request.method == 'GET':
        return jsonify({"status": "OK"})
