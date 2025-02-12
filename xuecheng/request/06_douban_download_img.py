import requests


def download_img(url,title):
    r = requests.get(url)
    with open(f'./file/{title}.png', 'wb') as f:
        f.write(r.content)

if __name__ == '__main__':
    url = 'https://movie.douban.com/explore'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        "cookie": "bid=5vStbboxJiA; _ga=GA1.1.1864941792.1708510577; __utmv=30149280.27849; douban-fav-remind=1; _ga_RXNMP372GL=GS1.1.1709112405.3.0.1709112405.60.0.0; __utma=30149280.1864941792.1708510577.1709105718.1718862695.2; viewed=\"4836697_35301417\"; ll=\"118183\"; ap_v=0,6.0; dbcl2=\"278463150:FufdaptAQ9k\"; ck=rCuF; push_noty_num=0; push_doumail_num=0; frodotk_db='3fbb812dc8f55e7fbf3283895ae01b7d'",
        "referer": url
    }
    resp = requests.get('https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=20&count=20&selected_categories=%7B%7D&uncollect=false&tags=&ck=rCuF', headers=headers)
    items = resp.json()['items']
    for item in items:
        try:
            print(item['title'])
            print(item['pic']['normal'])
            download_img(item['pic']['normal'],item['title'])
        except Exception as e:
            print(e)
