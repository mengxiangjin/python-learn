import time
import re
import requests
import base64

from urllib.parse import unquote
from bs4 import BeautifulSoup
from ZMQM3U8Downloader import ZMQM3U8Downloader
from enum import Enum

current_page = 1
movie_task = []

actor_name = '爱开发的'
actor_id = '19'
keyword = '夫妻主'
download_dir = 'D:\\taolu\\'
url = 'https://www.zimuquan2.uk'
actor_url_prefix = f'{url}/index.php/actor'
topic_url_prefix = f'{url}/index.php/topic'
search_url_prefix = f'{url}/index.php/vod/search'
zMQM3U8Downloader = None


headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
}


class ZMQ_TYPE(Enum):
    SELECTION_ACTOR_ID = 1
    SELECTION_SEARCH_KEYWORD = 2
    SELECTION_TOPIC_ID = 3



type = ZMQ_TYPE.SELECTION_ACTOR_ID

class Movie:
    def __init__(self, name, movie_id,m3u8_id, vod_url):
        self.name = name
        self.movie_id = movie_id
        self.vod_url = vod_url
        self.m3u8_id = m3u8_id
        self.movie_url = self.vod_url.rsplit('/', 1)[0] + "/index.m3u8"


# 根据js获取真正的html页面
def get_decoded_html(url):
    response = requests.get(url, headers=headers)

    # 提取Base64编码的内容
    match = re.search(r'atob\("([^"]+)"\)', response.text)
    if match:
        encoded_content = match.group(1)
        # Base64解码
        decoded_bytes = base64.b64decode(encoded_content)
        # URL解码
        final_html = unquote(decoded_bytes.decode('utf-8'))
        with open('res.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
        return final_html
    else:
        return "未找到编码内容"


#根据演员首字母搜索,返回演员字典
def get_actors_info(actor_letter='A'):
    actors_url = f'{actor_url_prefix}/show/letter/{actor_letter}.html'
    html_content = get_decoded_html(actors_url)
    with open('res.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    soup = BeautifulSoup(html_content, 'html.parser')

    div_content = soup.find('div', attrs={'class': 'van-grid'})
    a_tag = div_content.find_all('a')
    data_dict = {}
    for a in a_tag:
        href = f'{url}{a.get('href')}'
        name_tag = a.find('p', attrs={'class': 'name'})
        name = name_tag.get_text().strip()
        data_dict[href] = name
    print(data_dict)
    return data_dict

#获取专题页演员ID
def get_topic_info():
    actors_url = f'{topic_url_prefix}/index.html'
    html_content = get_decoded_html(actors_url)
    with open('res.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    soup = BeautifulSoup(html_content, 'html.parser')
    #
    a_tag_list = soup.find_all('a', attrs={'class': 'list_item'})
    data_dict = {}
    for a_tag in a_tag_list:
        href = f'{url}{a_tag.get('href')}'
        name = a_tag.find('div', attrs={'class': 'list_title'}).get_text().strip()
        counts = a_tag.find('div',attrs={'class': 'list_count'}).get_text().strip()
        data_dict[href] = name
    print(data_dict)
    return data_dict

#获取演员详细信息即作品列表
def get_actor_info():
    time.sleep(2)
    global current_page
    actor_url = f'{actor_url_prefix}/detail/id/{actor_id}.html?page={current_page}'
    html_content = get_decoded_html(actor_url)
    soup = BeautifulSoup(html_content, 'html.parser')

    movie_count = soup.find('div', attrs={'class': 'introduce_top'}).find('p',
                                                                          attrs={'class': 'count'}).get_text().strip()
    print(f'totals:{movie_count}--->page:{current_page}')

    #获取下面是所有的a标签
    a_tag = soup.find('div', attrs={'id': 'content'}).find_all('a')
    for a in a_tag:
        vod_url = a.find('img', attrs={'class': 'van-image__img md-lazy'}).get('data-src')
        name = a.find('div', attrs={'class': 'list_title'}).get_text().replace(' ', '')
        parts = a.get('href').split('/')
        movie_id = parts[parts.index('id') + 1]

        m3u8_id = vod_url.rsplit('/')[-2]
        print(f'图片地址：{vod_url} ---> 视频名称：{name}---> m3u8ID：{m3u8_id} ---> 视频ID：{movie_id}')
        movie_task.append(Movie(name, movie_id,m3u8_id, vod_url))
    disabled = soup.find('button', attrs={'class': 'btn-next'}).get('disabled')
    if disabled == 'disabled':
        start_download_movie_task()
    else:
        #还有下一页
        # current_page += 1
        # get_actor_info()
        start_download_movie_task()


def get_topic_info():
    time.sleep(2)
    global current_page
    actor_url = f'{topic_url_prefix}/detail/id/{actor_id}.html?page={current_page}'
    html_content = get_decoded_html(actor_url)
    soup = BeautifulSoup(html_content, 'html.parser')
    with open('res.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f'page:{current_page}')

    #获取下面是所有的a标签
    a_tag = soup.find('div', attrs={'id': 'content'}).find_all('a')
    for a in a_tag:
        vod_url = a.find('img', attrs={'class': 'van-image__img md-lazy'}).get('data-src')
        name = a.find('div', attrs={'class': 'list_title'}).get_text().replace(' ', '')
        parts = a.get('href').split('/')
        movie_id = parts[parts.index('id') + 1]

        m3u8_id = vod_url.rsplit('/')[-2]
        print(f'图片地址：{vod_url} ---> 视频名称：{name}---> m3u8ID：{m3u8_id} ---> 视频ID：{movie_id}')
        movie_task.append(Movie(name, movie_id,m3u8_id, vod_url))
    disabled = soup.find('button', attrs={'class': 'btn-next'}).get('disabled')
    if disabled == 'disabled':
        start_download_movie_task()
    else:
        #还有下一页
        # current_page += 1
        # get_actor_info()
        start_download_movie_task()


#关键词搜索
def search_key_word():
    time.sleep(2)
    global current_page
    global zMQM3U8Downloader
    if current_page == 1:
        search_url = f'{search_url_prefix}/wd/{keyword}.html'
    else:
        search_url = f'{search_url_prefix}/page/{current_page}/wd/{keyword}.html'

    html_content = get_decoded_html(search_url)
    with open('res.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    a_tag = soup.find('div', attrs={'id': 'content'}).find_all('a')
    for a in a_tag:
        vod_url = a.find('img', attrs={'class': 'van-image__img md-lazy'}).get('data-src')
        name = a.find('div', attrs={'class': 'list_title'}).get_text().replace(' ', '')
        parts = a.get('href').split('/')
        movie_id = parts[parts.index('id') + 1]
        m3u8_id = vod_url.rsplit('/')[-2]
        print(f'图片地址：{vod_url} ---> 视频名称：{name}---> m3u8ID：{m3u8_id} ---> 视频ID：{movie_id}')
        movie_task.append(Movie(name, movie_id,m3u8_id, vod_url))

    disabled = soup.find('button', attrs={'class': 'btn-next'}).get('disabled')
    if disabled == 'disabled':
        start_download_movie_task()
    else:
        #还有下一页
        # current_page += 1
        # search_key_word()
        start_download_movie_task()


# 开始下载任务
def start_download_movie_task():
    print('下载任务数--->', len(movie_task))
    for i, movie in enumerate(movie_task):
        print(f'视频名称：{movie.name} 视频ID：{movie.movie_id} 视频地址：{movie.movie_url} m3u8ID：{movie.m3u8_id}')
        zMQM3U8Downloader.set_download_url_dir(f'{movie.name}_{movie.m3u8_id}', movie.movie_url,
                                               f'{movie.name}_{movie.m3u8_id}')
        zMQM3U8Downloader.start_download()
        if i == 1:
            break
def init_dir():
    global zMQM3U8Downloader
    if type == ZMQ_TYPE.SELECTION_ACTOR_ID or type == ZMQ_TYPE.SELECTION_TOPIC_ID:
        zMQM3U8Downloader = ZMQM3U8Downloader(f'{download_dir}{actor_name}_{actor_id}')
    elif type == ZMQ_TYPE.SELECTION_SEARCH_KEYWORD:
        zMQM3U8Downloader = ZMQM3U8Downloader(f'{download_dir}{keyword}')


if __name__ == '__main__':
    #获取信息类的

    # actors_map = get_actors_info()
    # get_topic_info()

    # init_dir()
    # get_actor_info()
    # get_topic_info()
    # search_key_word()
    pass

