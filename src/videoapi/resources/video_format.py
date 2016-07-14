import re
import sys
from flask import request
from flask.ext import restful

from you_get.common import any_download


class Format(restful.Resource):
    def post(self):
        try:
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
        except:
            return {'error': 'arg error'}

    def get(self):
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
