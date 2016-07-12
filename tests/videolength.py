import json
import logging
import subprocess
from urllib.request import urlopen

import sys

VER = '0.98.91'

python_ver_str = '.'.join([str(i) for i in sys.version_info[:2]])
BILIGRAB_UA = 'Biligrab/{VER} (cnbeining@gmail.com) (Python-urllib/{python_ver_str}, like libcurl/1.0 NSS-Mozilla/2.0)'.format(VER = VER, python_ver_str = python_ver_str)


def getvideosize(url, verbose=False):
    try:
        if url.startswith('http:') or url.startswith('https:'):
            ffprobe_command = ['ffprobe', '-icy', '0', '-loglevel', 'repeat+warning' if verbose else 'repeat+error', '-print_format', 'json', '-select_streams', 'v', '-show_format', '-show_streams', '-timeout', '60000000', '-user-agent', BILIGRAB_UA, url]
        else:
            ffprobe_command = ['ffprobe', '-loglevel', 'repeat+warning' if verbose else 'repeat+error', '-print_format', 'json', '-select_streams', 'v', '-show_streams', url]
        logcommand(ffprobe_command)
        ffprobe_process = subprocess.Popen(ffprobe_command, stdout=subprocess.PIPE)
        try:
            ffprobe_output = json.loads(ffprobe_process.communicate()[0].decode('utf-8', 'replace'))
        except KeyboardInterrupt:
            logging.warning('Cancelling getting video size, press Ctrl-C again to terminate.')
            ffprobe_process.terminate()
            return 0, 0
        width, height, widthxheight, duration, total_bitrate = 0, 0, 0, 0, 0
        try:
            if dict.get(ffprobe_output, 'format')['duration'] > duration:
                duration = dict.get(ffprobe_output, 'format')['duration']
        except Exception:
            pass
        for stream in dict.get(ffprobe_output, 'streams', []):
            try:
                if duration == 0 and (dict.get(stream, 'duration') > duration):
                    duration = dict.get(stream, 'duration')
                if dict.get(stream, 'width')*dict.get(stream, 'height') > widthxheight:
                    width, height = dict.get(stream, 'width'), dict.get(stream, 'height')
                if dict.get(stream, 'bit_rate') > total_bitrate:
                    total_bitrate += int(dict.get(stream, 'bit_rate'))
            except Exception:
                pass
        if duration == 0:
            duration = int(get_url_size(url) * 8 / total_bitrate)
        return [[int(width), int(height)], int(float(duration))+1]
    except Exception as e:
        logorraise(e)
        return [[0, 0], 0]

#----------------------------------------------------------------------
def get_url_size(url):
    """str->int
    Get remote URL size by reading Content-Length.
    In bytes."""
    site = urlopen(url)
    meta = site.info()
    return int(meta.getheaders("Content-Length")[0])

#----------------------------------------------------------------------
def logcommand(command_line):
    logging.debug('Executing: '+' '.join('\''+i+'\'' if ' ' in i or '&' in i or '"' in i else i for i in command_line))


#----------------------------------------------------------------------
def logorraise(message, debug=False):
    if debug:
        raise message
    else:
        logging.error(str(message))

