import requests
import execjs
import time


def execute_js_challenge(js_code):
    """精确执行反爬虫JavaScript代码"""
    # 完整的JavaScript执行代码
    js_execution_code = """
    // 还原字符串数组
    var _0x49a6 = ["wyeCN", "4|2|0|3|1", "wQzOV", "split", "iTyzs", "pCQRM", "cookie", "location.href=location.href.replace(/[?|&]tads/, '')", "WTKkN", "bOYDu", "dtzqS"];

    // 字符串解密函数
    var _0x649a = function(a, n) {
        a -= 0;
        var e = _0x49a6[a];
        return e;
    };

    // 主函数
    function a(a) {
        function n() {
            for (var a = {
                wQzOV: _0x649a("0x4"),
                iTyzs: function(a, n) { return a + n; }
            }, n = a[_0x649a("0x5")][_0x649a("0x6")]("|"), e = 0; ;) {
                switch (n[e++]) {
                    case "0": t += "EO_Bot_Ssid="; continue;
                    case "1": return t;
                    case "2": t += ""; continue;
                    case "3": t = a[_0x649a("0x7")](t, 3439263744); continue;
                    case "4": var t = ""; continue;
                }
                break;
            }
        }

        var e = {
            WTKkN: 842897719,
            bOYDu: 282168727,
            dtzqS: function(a, n) { return a + n; },
            wyeCN: 893810107,
            pCQRM: function(a) { return a(); }
        }, t = 0;

        t += e[_0x649a("0x0")];
        t += e[_0x649a("0x1")];
        t = e[_0x649a("0x2")](t, e[_0x649a("0x3")]);

        return [t, e[_0x649a("0x8")](n)][a];
    }

    // 执行并返回结果
    var result1 = a(0);
    var result2 = a(1);

    return {
        cookie1: result1,
        cookie2: result2
    };
    """

    try:
        ctx = execjs.compile(js_execution_code)
        result = ctx.call("a", 0)  # 测试执行
        return {
            'cookie1': ctx.call("a", 0),
            'cookie2': ctx.call("a", 1)
        }
    except Exception as e:
        print(f"JavaScript执行错误: {e}")
        return None


def manual_calculate_cookies():
    """手动计算Cookie值（基于代码分析）"""
    # 分析代码逻辑：
    # a(0) = e.WTKkN + e.bOYDu + e.wyeCN
    # a(1) = "EO_Bot_Ssid=" + 3439263744

    cookie1 = 842897719 + 282168727 + 893810107
    cookie2 = "EO_Bot_Ssid=3439263744"

    return {
        'cookie1': str(cookie1),
        'cookie2': cookie2
    }


def download_video_with_cookies(video_url, output_filename="video.mp4"):
    """使用计算出的Cookie下载视频"""
    # 手动计算Cookie（更可靠）
    cookies_data = manual_calculate_cookies()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Referer': 'https://plays3.taolu.cloud/',
    }

    cookies = {
        '__tst_status': cookies_data['cookie1'],
        'EO_Bot_Ssid': cookies_data['cookie2'].split('=')[1]  # 只取值部分
    }

    # 添加时间戳防止缓存
    timestamp = int(time.time() * 1000)
    if '?' in video_url:
        final_url = f"{video_url}&_={timestamp}"
    else:
        final_url = f"{video_url}?_={timestamp}"

    try:
        print("使用计算的Cookie请求视频...")
        print(f"Cookie: {cookies}")

        response = requests.get(final_url, headers=headers, cookies=cookies, timeout=30, stream=True)

        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")

        if response.status_code == 200:
            total_size = int(response.headers.get('content-length'))
            accept_ranges = response.headers.get('accept-ranges', 'none')
            print(f"文件大小: {total_size} 字节")
            print(f"支持范围请求: {accept_ranges}")

            if accept_ranges != 'bytes':
                print("服务器不支持范围请求，使用普通下载")
                return
            else:
                # 使用范围请求分块下载
                chunk_size = 1024 * 1024  # 1MB chunks
                downloaded = 0

                with open(output_filename, 'wb') as f:
                    while downloaded < total_size:
                        # 计算当前块的范围
                        end = min(downloaded + chunk_size - 1, total_size - 1)
                        range_header = f"bytes={downloaded}-{end}"

                        headers_with_range = headers.copy()
                        headers_with_range['Range'] = range_header

                        try:
                            response = requests.get(video_url, headers=headers_with_range,
                                                    cookies=cookies, stream=True, timeout=30)
                            print('',response.status_code)
                            if response.status_code in (200, 206):  # 200 OK or 206 Partial Content
                                for chunk in response.iter_content(chunk_size=8192):
                                    if chunk:
                                        f.write(chunk)
                                        downloaded += len(chunk)
                                        print('正在下载中----',downloaded,total_size)
                                        print(f"进度: {downloaded}/{total_size} ({downloaded / total_size * 100:.1f}%)")

                                # 块之间添加延迟
                                time.sleep(0.5)
                            else:
                                print(f"范围请求失败: {response.status_code}")
                                break

                        except Exception as e:
                            print(f"块下载错误: {e}")
                            time.sleep(2)
                            continue

                if downloaded == total_size:
                    print(f"\n下载完成: {output_filename}")
                    return True
                else:
                    print(f"\n下载不完整: {downloaded}/{total_size}")
                    return False
        else:
            print(f"请求失败，状态码: {response.status_code}")

    except Exception as e:
        print(f"下载错误: {e}")

    return False

