#!/usr/bin/python3
'''
first endpoint (route) will be to return the status of your API
'''
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def storage_close(exception):
    '''
    method to handle @app.teardown_appcontext
    that calls storage.close()
    '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''
    returns a JSON-formatted 404 status code response
    '''
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", default="0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", default=5000)),
            threaded=True, debug=True)
