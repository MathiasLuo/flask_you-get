import json
import re
import time

import sys
from flask import request
from flask.ext import restful

from videoapi.common.util import getVideoJsonInfo
from you_get.common import any_download


class Urls(restful.Resource):
    def post(self):
        try:
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
        except:
            return {'error': 'args error',
                    'code': 404}

    def get(self, url):
        time1 = time.time()
        # url = request.form['url']
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
