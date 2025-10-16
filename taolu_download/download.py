import shutil

from utils import *
from m3u8Download import *


anchorUserId = '211367'
current_page = 1
max_page = 0
total_movie_counts = 0
nick_name = '缘彼S大大'
download_dir = 'E:\\taolu\\'

cloud_has_download_id = []

dir_name = f'{download_dir}{nick_name}_{anchorUserId}'

m3u8_downloader = M3U8Downloader(f'{dir_name}')

def create_dir():
    os.makedirs(dir_name,exist_ok=True)


def is_already_downloaded(movie_id):
    """检查文件是否已下载"""
    if str(movie_id) in cloud_has_download_id:
        return True
    # 遍历下载目录中的所有文件
    for filename in os.listdir(dir_name):
        file_path = os.path.join(dir_name, filename)

        # 如果是目录，继续遍历子目录
        if os.path.isfile(file_path) and str(movie_id) in filename:
            return True

    return False

def write_txt_flag():
    output_file = f'{dir_name}\\{nick_name}_{anchorUserId}.txt'
    if os.path.exists(output_file):
        os.remove(output_file)
    i = 0



    if len(cloud_has_download_id) != 0 and get_cloud_target_file() is not None:
        shutil.copy2(get_cloud_target_file(), output_file)

    with open(output_file, 'a', encoding='utf-8') as f:
        output_file_name = os.path.basename(output_file)
        for filename in os.listdir(dir_name):
            if filename == output_file_name:
                continue
            file_path = os.path.join(dir_name, filename)
            if os.path.isfile(file_path):
                i = i + 1
                f.write(filename + '\n')
    print(f'文件名已写入到 {output_file}---------> 写入的行数{i} ----------> 云视频数{len(cloud_has_download_id)}------>总视频数{total_movie_counts}')

def start_download(data_json):
    record_list = data_json['records']
    for movie_item in record_list:
        print('文件信息',movie_item)
        movie_item['videoTitle'] = movie_item['videoTitle'].replace(':','')
        movie_item['videoTitle'] = movie_item['videoTitle'].replace('/','')

        if is_already_downloaded(movie_item['id']):
            print(f'{movie_item['videoTitle']}_{movie_item['id']}已经下载过,主动跳过')
            continue
        print(f'开始下载----------->{movie_item['videoTitle']}_{movie_item['id']}-------->{movie_item['videoUrl']}')
        if str(movie_item['videoUrl']).endswith('.mp4'):
            start_download_mp4(movie_item)
        else:
            start_download_m3u8(movie_item)
    global current_page
    current_page = current_page + 1
    if current_page <= max_page:
        time.sleep(0.1)
        get_datas()
    else:
        #全部下载完成，写txt文件
        write_txt_flag()

def start_download_m3u8(movie_item):
    m3u8_downloader.set_temp_dir(f'{movie_item['videoTitle']}_{movie_item['id']}')
    success = m3u8_downloader.download_m3u8_to_mp4(movie_item['videoUrl'],f'{movie_item['videoTitle']}_{movie_item['id']}.mp4')
    if success:
        print(f"下载转换成功！---> {movie_item['videoTitle']} ---> {movie_item['videoUrl']}")
    else:
        print(f"下载转换失败！---> {movie_item['videoTitle']} ---> {movie_item['videoUrl']}")

def start_download_mp4(movie_item):
    vido_name = f'{movie_item['videoTitle']}_{movie_item['id']}.mp4'
    save_path = f'{dir_name}\\{vido_name}'
    try:
        # 发送GET请求，stream=True用于大文件
        headers =  {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'Referer': 'http://MAfAIOo0E8EMOWPA.black'
        }
        response = requests.get(movie_item['videoUrl'], headers=headers,stream=True, timeout=30)
        response.raise_for_status()  # 检查HTTP错误

        # 获取文件大小（可选）
        total_size = int(response.headers.get('content-length', 0))

        if total_size < 2000:
            print(f"\033[31m该url采用反爬机制---> {movie_item['videoUrl']} --->{vido_name}\033[0m")
            # download_video_with_cookies(movie_item['videoUrl'],save_path)
        else:
            # 下载文件
            with open(save_path, 'wb') as f:
                if total_size == 0:
                    # 没有内容长度信息，直接写入
                    f.write(response.content)
                    print(f"没有内容长度信息 下载完成: {save_path}")
                else:
                    # 显示进度条
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            # 显示进度
                            progress = (downloaded / total_size) * 100
                            print(f"\r下载进度: {progress:.1f}% ({downloaded}/{total_size} bytes)", end='')

                    print(f"\n下载完成: {save_path}")



    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")
        return None


def get_datas():
    url = f'https://proapi.taolu.cloud/live/live/video/anchor/{current_page}/10'

    params = get_request_params(anchorUserId, current_page)
    headers = get_request_headers()
    resp = requests.get(url=url, params=params, headers=headers)

    resp_json = resp.json()
    if resp_json['code'] == 20000:
        global max_page
        global total_movie_counts
        if max_page == 0:
            total_movie_counts = resp_json['data']['total']
            max_page = total_movie_counts / 10 + 1
            print(f'总视频数目--->{total_movie_counts} 最大page数--->{max_page}')
        # 请求成功
        start_download(resp_json['data'])
    else:
        # 请求失败
        print(f'请求失败---->{resp_json['code']}')

def init_cloud_has_download_ids():
    target_file = get_cloud_target_file()
    if target_file is not None:
        with open(target_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and '_' in line:
                    id = line.split('_')[-1].split('.')[0]
                    cloud_has_download_id.append(id)


def get_cloud_target_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(current_dir):
        if anchorUserId in filename and os.path.isfile(os.path.join(current_dir, filename)):
            return os.path.join(current_dir, filename)
    return None

if __name__ == '__main__':
    init_cloud_has_download_ids()
    create_dir()
    get_datas()