#!/usr/bin/python3
'''Flask App Blueprint Setup'''
from api.v1.views import app_views
from flask import Flask
from os import getenv
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardowni_db(exception):
    '''Closes connection to storage'''
    if storage is not None:
        storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
