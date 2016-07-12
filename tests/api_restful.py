import re
import sys
import json
from flask import request
from flask import Flask

from you_get.common import any_download


class TextArea(object):
    def __init__(self):
        self.buffer = []

    def write(self, *args, **kwargs):
        self.buffer.append(args)


app = Flask(__name__)

stdout = sys.stdout
sys.stdout = TextArea()


@app.route('/')
def hello_word():
    return 'hello word'


@app.route('/format', methods=['POST'])
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


@app.route('/api', methods=['POST'])
def get_urls():
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
    for s in text_area.buffer:
        for str in s:
            if re.findall(r'(http://[^?]+)', str):
                api_list = str
    return json.dumps({'url': api_list})


if __name__ == '__main__':
    app.run()
