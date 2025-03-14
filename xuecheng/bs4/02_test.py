import json
import os
import shutil

import requests
import time
import re
from bs4 import BeautifulSoup

class Bean:
    score = None
    title = None
    href = None
    progress = None
    category = None
    area = None
    year = None
    actor = None
    director = None
    update_date = None
    content = None


def get_details(url,status,title,category):
    bean = Bean()

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div',attrs={'class':'stui-content__detail'})
    href = f'https://www.duanjuwang.cc/{soup.find('div',attrs={'class':'stui-content__thumb'}).find('img').attrs['data-original']}'
    progress = soup.find('div',attrs={'class':'stui-content__thumb'}).find('span',attrs={'class':'pic-text text-right'}).text

    head = content_div.find('h1').text
    score = content_div.find('span').text
    title = head.replace(score,'')

    bean.score = score
    bean.title = title
    bean.href = href
    bean.progress = progress
    print(score,end=' ')
    print(title,end=' ')
    print(href,end=' ')
    print(progress,end=' ')
    p_list = content_div.find_all('p',class_=['data'])

    my_list = []

    for p in p_list:
        data_iter = list(p.strings)
        for i in data_iter:
            str = re.sub(r'[\s\n]+', '', i)
            if len(str) > 0:
                print(str,end="")
                my_list.append(str)
    bean.category = my_list[1]
    bean.area = my_list[3]
    bean.year = my_list[5]
    bean.actor = my_list[7]
    bean.director = my_list[9]
    bean.update_date = my_list[11]

    desc = soup.find('div',attrs={'id':'desc'}).find('p').text
    bean.description = desc.replace(',想要看更多由未知主演的相关影视作品，请关注www.duanjuwang.cc！','')

    print(desc)
    result_list.append(bean)
    print(result_list)


def rename_files_in_folder(folder_path, prefix):
    index = 1
    # 获取文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 检查是否是文件（排除文件夹）
        if os.path.isfile(file_path):
            # 构造新的文件名
            new_filename = f"{prefix}{index}.png"
            new_file_path = os.path.join(folder_path, new_filename)

            # 重命名文件
            os.rename(file_path, new_file_path)
            print(f"重命名文件: {filename} -> {new_filename}")
            index = index + 1
        else:
            for filename2 in os.listdir(file_path):
                file_path_2 = os.path.join(file_path, filename2)
                # 构造新的文件名
                new_filename = f"{prefix}{index}.png"
                new_file_path = os.path.join(file_path, new_filename)

                # 重命名文件
                os.rename(file_path_2, new_file_path)
                print(f"重命名文件: {filename} -> {new_filename}")
                index = index + 1

def move_files_in_folder(folder_path):
    target_path = 'C:/Users/hh/Desktop/安静书素材/手账素材/beijing'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # 检查是否是文件（排除文件夹）
        if os.path.isfile(file_path):
            dest_file_path = os.path.join(target_path, filename)
            shutil.move(file_path, dest_file_path)
        else:
            for filename2 in os.listdir(file_path):
                file_path_2 = os.path.join(file_path, filename2)
                dest_file_path = os.path.join(target_path, filename2)
                shutil.move(file_path_2, dest_file_path)
                print(f"文件 {filename2} 已成功移动到 {dest_file_path}")

if __name__ == '__main__':
    # 示例使用
    # folder_path = 'C:/Users/hh/Desktop/安静书素材/手账素材/背景'  # 替换为你的文件夹路径
    # prefix = 'shouzhang_beijing_'  # 文件名前缀
    # rename_files_in_folder(folder_path, prefix)
    # move_files_in_folder(folder_path)


    result_list = []
    url = 'https://www.duanjuwang.cc'
    response = requests.get(f'{url}/vodtype/duanju.html')
    soup = BeautifulSoup(response.text, 'html.parser')
    div_list = soup.findAll('div',attrs={'class':'stui-pannel stui-pannel-bg clearfix'})[1:]
    for div in div_list:
        category = div.find('h3',attrs={'class':'title'}).text
        li_list = div.find('ul',attrs={'class':'stui-vodlist clearfix'}).findAll('li')

        for li in li_list:
            status = li.find('span',attrs = {'class': 'pic-text text-right'}).text
            href = li.find('h4').find('a')['href']
            title = li.find('h4').find('a').text
            # print(status,href,title,category)
            get_details(f'{url}{href}',status,title,category)
            time.sleep(1)
        #     break
        # if len(result_list) == 3:
        #     break
    result_list = [bean.__dict__ for bean in result_list]
    with open('data.json','w',encoding='UTF-8') as f:
        json.dump(result_list,f,ensure_ascii=False)

