import re
from _codecs import encode

from you_get.common import any_download, any_download_playlist
from you_get.extractors.le import decode


# any_download('http://www.le.com/ptv/vplay/25520328.html',info_only=False, output_dir='.', merge=False)
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

# print(urls)
# videos = Youku.oset(urls)
