import requests


#可直接通过request 在请求头添加登录之后的cookie获取书架列表信息 前提：需要在浏览器登录并手动拿到cookie
headers = {
    'cookie': 'GUID=4927006c-ac8c-4167-90d2-8e7b176fc7d1; sajssdk_2015_cross_new_user=1; BAIDU_SSP_lcr=https://www.baidu.com/link?url=QiAk8d_CypaSsBStDrS5BxoOo-39dLQCanO34oZPVNu&wd=&eqid=c75015be0132465e0000000667579b08; Hm_lvt_9793f42b498361373512340937deb2a0=1733794573; HMACCOUNT=E5395DC947B2D9B5; acw_sc__v2=67579c6ff5fd43eb3ebdbb47508cfe420f546bd9; c_channel=0; c_csc=web; accessToken=avatarUrl%3Dhttps%253A%252F%252Fcdn.static.17k.com%252Fuser%252Favatar%252F15%252F55%252F25%252F103902555.jpg-88x88%253Fv%253D1733794995000%26id%3D103902555%26nickname%3D%25E4%25B8%2580%25E4%25BC%2591Plus%26e%3D1749347154%26s%3Dc583a20b8d4f7596; tfstk=fyMIgqM0rwbIgtReGgKa5mh9xDySO492dgZ-m0BF2JeK28i-qzzUazl_Bo33wvyEYVtSWqmUaJHSsTimqv-3UH2nx82JuEJqFDm3EBl3TADQB1EjXuQ8eHokMWyJuEJN_GFH883F-GNlCcUgVuU8e4I9fuZze9FRp1QTSPU8e7CKXcEYvTBLykKsXPq8ezhroKZGcPiBbVl-FYpf6Da1ets00WImx_WV3AZQOYn_5WNICkNQk5mEtAHK70HEK5AG_8mZG4G-kF5UJjZj5SlBl9gj-u3_LxKkt5V-FYZisU17lbnEibF6vpn_dyN_AWsCwJG--YNnOgxmXJ3iirVpsFqsLxP7o5_9Jco_JSGS8FX88jit5SkN7tyxiVM7M-Ir5tzbzU15fSX8fr-6f_fobzvjUOhpEQNLjluwfh1cIWEgfr-6f_fu9lqabht1iOf..; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22103902555%22%2C%22%24device_id%22%3A%22193ae35a61290d-059c5eced146a5-26011851-1058400-193ae35a6131e4c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%2C%22first_id%22%3A%224927006c-ac8c-4167-90d2-8e7b176fc7d1%22%7D; ssxmod_itna=QqAx2Qi=GQ0=itN40LP0PDQ9cnnKqioKoe=KDBnhhcx05geGzDAxn40iDt=OTG98xIPo0mYhL+qSjDG=7Ch+DWqthtRGdA6QQx0aDbqGkqBA4iiSDCeDIDWeDiDG4GmeqGtDpxG=DjDytZ9TtDm4GWDeDgDqGg3erD03NBWdrD4qDBAxQDKw2g0DDl7hp5twG5ieD+Dd2lBlUxWcDqGqDM7eGXbYHQGqT1gPwVWaF8=nPcDB=pxBjZIntt67UDgu03Y0pPAYYai4hWmDwx8+4q83hID2wWSBmxYxPUNs+S2DDAm7+eSiD===; ssxmod_itna2=QqAx2Qi=GQ0=itN40LP0PDQ9cnnKqioKoe=KDBnhhxnFdE5xDsD9WNDjRb=FzCq8qigqidmf6qPheu3fuiUzt=eZYIegYBDcDf/bf0gG5VRKjKcCS3Qt5fcKAb7=C2NTzdtazVAvRh5bqPLFYdRI2wC3+Ux0Y2sROeYk7=8Q7hCfnwhio2mt3j5d8xBY16IU8TSY7n4lk=X+4jnAduFhn5Tbn5s8wmClaUPn2HXC7vcF7jHNcG1oPumrQxj4/v4znvA3gxvfERPzY3NF7n/Y=uiKddbdkDg33xiLgZnzfZe7kWip/tLtmHtR+iGRIhttbp8u4ReEjuRt0+K+pI2FFmBia+8H7GYx=wCCmeHuw+7rWAH4Eo5O+j+tYGy393dBEimxSvFze4unq8G=Fm1So4u4rlElnbTAuTmmCjbW0cj/xKbTqoyDbqWoemCIqn8IfbNESrvr7o8TpRRG3xUnc7irwben8WF5W1nQ99tl0ynn8U5CR4UKBDLrl8A1AhrNRhCcNgLT8A+aqwnRR8AHHHF4q7HTKovx=4g9PWdx=l8wNu3unhYZI50RCg8lINWvCm=jhek8idD07l7dBGH834Ir9c0yRR5AAzTFbeYLag=3y+7SBXxPvxgvGpaVS7kDD7=DYKKeD===; Hm_lpvt_9793f42b498361373512340937deb2a0=1733795540'
}
resp = requests.get('https://user.17k.com/ck/author2/shelf?page=1&appKey=2406394919',headers = headers)
print(resp.json())


#程序模拟登录，自动获取到cookied，请求拿到书架信息
session = requests.session()
session.get('login',data= {
    'username': '<EMAIL>',
    'password': '<PASSWORD>',
})
#session去登录,登录成功后，服务器会返回客户端cookie，客户端拿到此cookie，保存，下次请求是在请求头添加此cookie
session.headers.update(headers)
#session中已存在cookie，可直接获取到书架信息
session.get('https://user.17k.com/ck/author2/shelf?page=1&appKey=2406394919')