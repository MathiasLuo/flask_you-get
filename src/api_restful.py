import json
import re
import sys
import time

from flask import Flask
from flask import request
from flask.ext.restful import Resource, Api
from werkzeug.contrib.fixers import ProxyFix

from you_get.common import any_download

errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 500,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 405,
        'extra': "Any extra information you want.",
    },
}


class TextArea(object):
    def __init__(self):
        self.buffer = []

    def write(self, *args, **kwargs):
        self.buffer.append(args)

    def flush(self, *args, **kwargs):
        pass


app = Flask(__name__)
api = Api(app, errors=errors, catch_all_404s=True)

stdout = sys.stdout
sys.stdout = TextArea()


class Format(Resource):
    def post(self):
        url = request.form['url']
        sys.stdout.buffer = []
        any_download(url, info_only=True, output_dir='.',
                     merge=False)
        text_area = sys.stdout
        format_list = []
        for s in text_area.buffer:
            for str in s:
                if re.findall(r'(\s*- format:.*)', str):
                    format_list.append(str.strip()[9:].strip())
        return {'format': format_list}


class Urls(Resource):
    def post(self):
        time1 = time.time()
        url = request.form['url']
        sys.stdout.buffer = []
        if 'format' in request.form:
            ft = request.form['format']
            any_download(url, info_only=False, output_dir='.',
                         merge=False, format=ft)
        else:
            any_download(url, info_only=False, output_dir='.',
                         merge=False)
        text_area = sys.stdout
        api_list = ''
        for s in text_area.buffer:
            for str in s:
                if re.findall(r'(http://[^?]+)', str):
                    api_list = str

        if 'time' in request.form:
            if request.form['time']:
                urls_json = []
                video_list = api_list.replace("'", "").split(',')
                for index in range(len(video_list)):
                    u = video_list[index].strip()
                    video_json = json.loads(getVideoJsonInfo("%s" % u))
                    time_length = video_json['format']['duration']
                    file_size = video_json['format']['size']
                    urls_json.append({
                        "size": file_size,
                        "seconds": time_length,
                        "number": index,
                        "url": u
                    })
                time2 = time.time()
                return {'url': urls_json,
                        'parse_time': time2 - time1}

        time2 = time.time()
        return {'url': api_list,
                'parse_time': time2 - time1}


class HelloWorld(Resource):
    def get(self):
        return {'url': "hello world"}


api.add_resource(Format, "/format")
api.add_resource(Urls, "/urls")
api.add_resource(HelloWorld, '/')


@app.errorhandler(Exception)
def handle_invalid_usage(error):
    from flask import jsonify

    response = jsonify({
        'error': hasattr(error, 'error') and error.error or 'Unexpected Error!!!',
        'error_description': hasattr(error,
                                     'description') and error.description or
                             'The system has encountered an unexpected error. Please contact administrator (hoanggia.lh@gmail.com) for better supports',
        'message': error.message,
        'status_code': hasattr(error, 'status_code') and error.status_code or 500,
    })

    response.status_code = hasattr(error, 'status_code') and error.status_code or 500
    return response


@app.route('/')
def hello_word():
    return 'hello word'


@app.route('/formats', methods=['POST', 'GET'])
def get_formats():
    url = request.form['url']
    sys.stdout.buffer = []
    any_download(url, info_only=True, output_dir='.',
                 merge=False)
    text_area = sys.stdout
    format_list = []
    for s in text_area.buffer:
        for str in s:
            if re.findall(r'(\s*- format:.*)', str):
                format_list.append(str.strip()[9:].strip())
    return json.dumps({'format': format_list})


@app.route('/api', methods=['POST', 'GET'])
def get_urls():
    time1 = time.time()
    url = request.form['url']
    sys.stdout.buffer = []
    if 'format' in request.form:
        ft = request.form['format']
        any_download(url, info_only=False, output_dir='.',
                     merge=False, format=ft)
    else:
        any_download(url, info_only=False, output_dir='.',
                     merge=False)
    text_area = sys.stdout
    api_list = ''
    for s in text_area.buffer:
        for str in s:
            if re.findall(r'(http://[^?]+)', str):
                api_list = str

    if 'time' in request.form:
        if request.form['time']:
            urls_json = []
            video_list = api_list.replace("'", "").split(',')
            for index in range(len(video_list)):
                u = video_list[index].strip()
                video_json = json.loads(getVideoJsonInfo("%s" % u))
                time_length = video_json['format']['duration']
                file_size = video_json['format']['size']
                urls_json.append({
                    "size": file_size,
                    "seconds": time_length,
                    "number": index,
                    "url": u
                })
            time2 = time.time()
            return json.dumps({'url': urls_json,
                               'parse_time': time2 - time1})

    time2 = time.time()
    return json.dumps({'url': api_list,
                       'parse_time': time2 - time1})


app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
