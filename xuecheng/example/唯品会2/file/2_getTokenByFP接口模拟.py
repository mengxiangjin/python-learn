import requests

if __name__ == '__main__':
    url = 'https://vcsp-api.vip.com/token/getTokenByFP'
    resp = requests.get(url, headers={'vcspauthorization': 'vcspSign=05a68135d2bfd322e3a22f95bbc25a24c777f387'},
                 params={'vcspKey': '4d9e524ad536c03ff203787cf0dfcd29'},verify=False
             )
    print(resp.json())
    pass