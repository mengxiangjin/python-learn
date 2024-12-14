#梨视频
#https://video.pearvideo.com/mp4/short/20241028/cont-1796875-16039438-hd.mp4
#https://video.pearvideo.com/mp4/short/20241028/1733916689341-16039438-hd.mp4
#json返回的视频播放地址，实际不能正确播放，观察到1733916689341实际为json数据中的time，将其替换为cont-1796875即可访问到真实数据，1796875是此视频的id
import requests


headers = {
    #有些网站防盗链，会判断你是从哪个起点进入的，没有上一级，会被网站限制访问，所以需要在头部添加此referer
    'referer' : "https://www.pearvideo.com/video_1796875"
}

video_id = '1796875'
url = 'https://www.pearvideo.com/video_' + video_id
new_url = 'https://www.pearvideo.com/videoStatus.jsp?contId=1796875&mrd=0.30785681211784444'
r = requests.get(new_url,headers=headers)

#正常请求到数据，需要观察其数据结构模式
json_data = r.json()
current_time = json_data['systemTime']
temp_download_url = json_data['videoInfo']['videos']['srcUrl']
rs = str(temp_download_url).replace(current_time,'cont-' + video_id)
with open('video.mp4','wb') as f:
    resp = requests.get(rs)
    f.write(resp.content)
print('over')
f.close()
r.close()
