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


def getVideoSize(url):
    s = os.popen('ffprobe -v quiet -print_format json -show_format -show_streams "%s"' % url).read()
    print(s)


if __name__ == '__main__':
    time0 = time.time()
    li = []
    for i in li:
        getVideoSize(i)
    time1 = time.time()
    print('time ---------------------------------')
    print(time1 - time0)
