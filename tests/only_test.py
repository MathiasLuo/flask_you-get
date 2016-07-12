import os
import re
from _codecs import encode

from tests.videolength import getvideosize
from you_get.common import any_download, any_download_playlist
from you_get.extractors.le import decode


class TextArea(object):
    def __init__(self):
        self.buffer = []

    def write(self, *args, **kwargs):
        self.buffer.append(args)


import sys

# stdout = sys.stdout
# sys.stdout = TextArea()

# print to TextArea
# print('testA')
# print("testB")
# print("testC")

any_download('', info_only=True, output_dir='.', merge=False)

# getvideosize("http://119.84.32.111/185/9/87/letv-uts/19/ver_00_22-1054325318-avc-3125741-aac-128000-1899280-775274370-e4a7e8dbcc2c80345d1f864a0e1d7531-1467956300969_mp4/ver_00_22_0_0_1_2310144_0_0.ts?mltag=8888&platid=1&splatid=101&playid=0&geo=CN-22-296-1&tag=letv&ch=&p1=&p2=&p3=&tss=ios&b=3265&bf=90&nlh=4096&path=&sign=letv&proxy=2002002639,3684256367,1778917252&uuid=&ntm=1468303800&keyitem=GOw_33YJAAbXYE-cnQwpfLlv_b2zAkYctFVqe5bsXQpaGNn3T1-vhw..&its=0&nkey2=747faaf109c4f6fbd39ef02eb9bfa3f3&uid=2002002105.rp&qos=5&enckit=&m3v=1&token=&vid=&liveid=&station=&app_name=&app_ver=&fcheck=0&pantm=&panuid=&pantoken=&cips=219.152.27.243&vod_live_path=")

# text_area, sys.stdout = sys.stdout, stdout

# print to console
# print(text_area.buffer)

# a = 'VC_015PТ4U'.decode('utf-8')
# print(len(a))
# print(a)
# print(a[0])
# a = '123qwe'
# print(ord('1'))
# print(isinstance(1,int))
# a = os.popen('python api.py').read()
# os.popen("from you_get.common import any_download")
# a = os.popen('python api.py').read()
# a = os.popen("any_download('http://v.qq.com/cover/m/mhaqxv1yyo609jc.html', info_only=False, output_dir='.', merge=False)").read()
# print(a)
# a = any_download('http://v.qq.com/cover/m/mhaqxv1yyo609jc.html', info_only=False, output_dir='.', merge=False)

# --->> 直接下载:
# any_download_playlist('http://v.youku.com/v_show/id_XMTYxNDc4NzM3Mg==.html?from=y1.3-idx-beta-1519-23042.223465.2-1', info_only=False, output_dir='.', merge=False)

# --->> 根据链接判断 print(url_to_module('http://v.youku.com/v_show/id_XMTYxNDc4NzM3Mg==.html?from=y1.3-idx-beta-1519-23042.223465.2-1'))
# --->> 获取搜索界面
# http://www.youku.com/playlist_show/id_youku.com/v_show/id_XMTYxNTkzMjI5Mg==.html?from=y1.3-idx-beta-1519-23042.223465.1-1
# video_page = get_content( "http://www.youku.com/playlist_show/id_youku.com/v_show/id_XMTYxNTkzMjI5Mg==.html?from=y1.3-idx-beta-1519-23042.223465.1-1")
# print(s)

# urls  = re.findall(r'href="(http://v\.youku\.com/[^?"]+)',video_page)
# urls = re.findall('href="(http://www\.youku\.com/playlist_show/id_XMTYxNTkzMjI5Mg==.html?from=y1.3-idx-beta-1519-23042.223465.1-1_[^?"]+)',video_page)
# print(urls)

# videos = Youku.oset(urls)
