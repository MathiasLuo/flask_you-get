import re
import sys

from you_get.common import any_download


class TextArea(object):
    def __init__(self):
        self.buffer = []

    def write(self, *args, **kwargs):
        self.buffer.append(args)


stdout = sys.stdout
sys.stdout = TextArea()

any_download('http://v.youku.com/v_show/id_XMTYzODcxMTg2NA==.html?f=27619333', info_only=True, output_dir='.',
             merge=False)

text_area, sys.stdout = sys.stdout, stdout

a = []

for s in text_area.buffer:
    for str in s:
        if re.findall(r'(\s{4}- format:.*)', str):
            print(str[13:].strip())
            a.append(str[13:])
