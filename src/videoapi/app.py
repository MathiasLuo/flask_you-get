import sys

import flask_restful
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from videoapi.common import errors
from videoapi.common.textUtil import TextArea
from videoapi.resources.hello_world import HelloWorld
from videoapi.resources.video_format import Format
from videoapi.resources.video_urls import Urls

app = Flask(__name__)
api = flask_restful.Api(app, errors=errors)

stdout = sys.stdout
sys.stdout = TextArea()

api.add_resource(HelloWorld, "/")
api.add_resource(Format, "/format")
api.add_resource(Urls, "/urls")

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
