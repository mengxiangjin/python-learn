
import requests
import re

import asyncio
import aiofiles
import aiohttp

from bs4 import BeautifulSoup

domain = 'https://m.feilusw.com'
url = 'https://m.feilusw.com/shu/3398/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Cookie': 'user_sex=3128; Hm_lvt_2c3581ea8095bf5237760a5cc7ea14d9=173638823'
              '0; HMACCOUNT=E5395DC947B2D9B5; Hm_lvt_0912763a71919ffeffd7b7bdfd314fb5=1736390091; Hm_lvt_1bc7ea5d4c32d7aef626aabcc3507063=1736390091; novel_3398=3268806%7C1736390214; Hm_lpvt_0912763a71919ffeffd7b7bdfd314fb5=1736390259; Hm_lpvt_1bc7ea5d4c32d7aef626aabcc3507063=1736390259; vv=1736390281; qd_vt=1736390281; Hm_lpvt_2c3581ea8095bf5237760a5cc7ea14d9=1736390326'
}

async def get_chapter_page(url):
    chapter_list = []
    obj = re.compile(r"href='/(?P<href>.*?)'", re.S)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            iter = obj.finditer(await resp.text())
            for match in iter:
                chapter_list.append(f'{domain}/{match.group('href')}')

    for chapter in chapter_list:
        await download_page(chapter)
    # resp = requests.get(url, headers=headers)


    # iter = obj.finditer(resp.text)
    # chapter_list = []
    # for match in iter:
    #     chapter_list.append(f'{domain}/{match.group('href')}')
    # for chapter in chapter_list:
    #     download_page(chapter)

async def download_page(chapter_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(chapter_url, headers=headers) as resp:
            soup = BeautifulSoup(await resp.text(), 'html.parser')
            try:
                title = soup.find('div', attrs={'id': 'nr_title'}).text.strip()
            except AttributeError:
                print("error:" + chapter_url)
            print(f'开始下载{title}')
            content_list = soup.find('div', attrs={'id': 'nr_body'}).find_all('p')
            async with aiofiles.open(f'book.txt', mode='a', encoding='utf-8') as f:
                await f.write(f'{title}\n')
                for content in content_list:
                    await f.write(f'{content.text}\n')
                print(f'下载完成{title}')

            next_page = soup.find_all('a', attrs={'class': 'Readpagebtn'})
            for page in next_page:
                if page.text == '下一页':
                    await download_page(f'{domain}{page["href"]}')
                    break




    # resp = requests.get(chapter_url, headers=headers)
    # soup = BeautifulSoup(resp.text, 'html.parser')
    # title = soup.find('div', attrs={'id': 'nr_title'}).text.strip()

    # print(f'开始下载{title}')
    # content_list = soup.find('div', attrs={'id': 'nr_body'}).find_all('p')

    # with open('book.txt', 'a', encoding='utf-8') as f:
    #     f.write(f'{title}\n')
    #     for content in content_list:
    #         f.write(f'{content.text}\n')
    # print(f'下载完成{title}')

    next_page = soup.find_all('a', attrs={'class': 'Readpagebtn'})
    for page in next_page:
        if page.text == '下一页':
            await download_page(f'{domain}{page["href"]}')
            break

async def main(url_list):
    task = []
    for url in url_list:
        task.append(asyncio.create_task(get_chapter_page(url)))
    await asyncio.gather(*task)

if __name__ == '__main__':
    resp = requests.get('https://m.feilusw.com/shu/3398/', headers=headers)
    url_list = []
    soup = BeautifulSoup(resp.text, 'html.parser')
    option_list = soup.find('select').find_all('option')
    for option in option_list:
        url_list.append(f'{domain}{option["value"]}')
    asyncio.run(main(url_list))
    resp.close()
    # obj = re.compile(r"href='/(?P<href>.*?)'",re.S)
    # resp = requests.get(url,headers=headers)
    # url_list = []
    # soup = BeautifulSoup(resp.text, 'html.parser')
    # option_list = soup.find('select').find_all('option')
    # for option in option_list:
    #     url_list.append(f'{domain}{option["value"]}')
    # for url in url_list:
    #     get_chapter_page(url)
    #     time.sleep(1)
