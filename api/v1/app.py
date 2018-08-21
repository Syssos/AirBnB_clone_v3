 #!/usr/bin/python3
from flask import Flask, Blueprint, make_response, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(self):
    """ calls close to close session
    """
    storage.close()

@app.errorhandler(404)

def errorhandler(error):
    """ Returns status 404 Not found
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    var = {'host': '0.0.0.0', 'port': 5000}
    if getenv('HBNB_API_PORT'):
        var['port'] = getenv('HBNB_API_PORT')
    if getenv('HBNB_API_HOST'):
        var['host'] = getenv('HBNB_API_HOST')
    app.run(host=var.get('host'), port=var.get('port'), threaded=True)
