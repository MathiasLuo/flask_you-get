import os
import re

import time

import time
from functools import wraps


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total time running %s: %s seconds" %
              (function.func_name, str(t1 - t0))
              )
        return result

    return function_timer


def getVideoJsonInfo(url):
    video_json = os.popen('ffprobe -v quiet -print_format json -show_format -show_streams "%s"' % url).read()
    return video_json


