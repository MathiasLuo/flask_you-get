import re
import sys
import json

import time
from flask import request
from flask import Flask

from tests.ffprobe_test import getVideoJsonInfo
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
    for s in text_area.buffer:
        for str in s:
            if re.findall(r'(http://[^?]+)', str):
                api_list = str

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
    time2 = time.time();
    return json.dumps({'url': urls_json,
                       'parse_time': time2 - time1})


if __name__ == '__main__':
    app.run(port=5001)
