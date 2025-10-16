import requests
import re
import subprocess
import os
import concurrent.futures
import random
import time

from Crypto.Cipher import AES
from urllib.parse import urljoin
from tqdm import tqdm
from pathlib import Path
import urllib3

#过滤控制台ssl警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ZMQM3U8Downloader:
    def set_download_url_dir(self, temp_dir_name, m3u8_url, output_name, max_workers=3):
        """设置临时目录"""
        self.temp_dir = self.output_dir / temp_dir_name
        self.temp_dir.mkdir(exist_ok=True)
        self.m3u8_url = m3u8_url
        self.base_url = '/'.join(m3u8_url.split('/')[:-1]) + '/'
        self.ts_name_files = []
        self.ts_files = []
        self.key = None
        self.output_name = output_name
        self.max_workers = max_workers

    def __init__(self, output_dir):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        }
        self.max_workers = None
        self.output_name = None
        self.key = None
        self.ts_name_files = None
        self.ts_files = None
        self.base_url = None
        self.m3u8_url = None
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = None

    def start_download(self):
        """极速下载并转换"""
        print("🚀 启动极速下载模式...")

        # 解析m3u8
        response = requests.get(self.m3u8_url,headers=self.headers)
        content = response.text

        # 获取密钥
        key_match = re.search(r'URI="([^"]+)"', content)
        if key_match:
            key_url = urljoin(self.base_url, key_match.group(1))
            self.key = requests.get(key_url).content

        # 获取TS列表
        self.ts_name_files = re.findall(r'^\d+\.ts$', content, re.MULTILINE)

        # 多线程下载
        print(f"📥 并发下载 {len(self.ts_name_files)} 个文件...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(tqdm(executor.map(self._download_ts_with_retry, self.ts_name_files), total=len(self.ts_name_files)))

        # 过滤掉下载失败的文件
        self.ts_files = [result for result in results if result is not None]
        self.ts_files.sort()
        if len(self.ts_files) != len(self.ts_name_files):
            print('下载文件不完整，请检查并重试')
            self._retry_failed_segments()

        # 再次检查完整性
        if len(self.ts_files) != len(self.ts_name_files):
            print(f'❌ 最终下载不完整: {len(self.ts_files)}/{len(self.ts_name_files)}，请检查网络连接')
            return False

        merged_ts = self._merge_segments()
        # 4. 转换为mp4
        print("正在转换为mp4...")
        if not self.output_name.endswith('.mp4'):
            self.output_name += '.mp4'

        self._convert_to_mp4(merged_ts, self.output_dir / self.output_name)
        print(f"转换完成: {self.output_dir / self.output_name}✅")

        print("开始清理临时文件...")
        # 5. 清理临时文件
        self._cleanup(merged_ts)
        print('清理临时文件完成✅')
        print("🎉 极速下载完成！✅")
        return True

    def _merge_segments(self):
        """合并所有ts文件为一个文件"""
        merged_file = self.temp_dir / "merged.ts"

        with open(merged_file, 'wb') as outfile:
            for ts_file in tqdm(self.ts_files, desc="合并进度"):
                with open(ts_file, 'rb') as infile:
                    outfile.write(infile.read())

        return merged_file

    def _download_ts_with_retry(self, ts_file):
        """带重试机制的TS文件下载"""
        max_retries = 3
        base_delay = 1

        for attempt in range(max_retries):
            try:
                # 添加随机延迟，避免请求过于频繁
                delay = random.uniform(0.5, 2.0) + (attempt * 0.5)
                if attempt > 0:
                    print(f"⏳ 第 {attempt + 1} 次重试 {ts_file}，等待 {delay:.1f} 秒...")
                    time.sleep(delay)

                ts_url = self.base_url + ts_file
                response = requests.get(ts_url, headers=self.headers, timeout=30, verify=False)
                response.raise_for_status()

                if self.key:
                    cipher = AES.new(self.key, AES.MODE_CBC, iv=b'\x00' * 16)
                    decrypted = cipher.decrypt(response.content)
                    # 简单填充处理
                    if decrypted[-1] <= 16:
                        decrypted = decrypted[:-decrypted[-1]]
                else:
                    decrypted = response.content

                # 修正：直接使用原始文件名
                filepath = self.temp_dir / ts_file
                with open(filepath, 'wb') as f:
                    f.write(decrypted)

                print(f"✅ 下载完成: {ts_file} ({len(decrypted)} bytes)")
                return filepath

            except requests.exceptions.RequestException as e:
                error_type = type(e).__name__
                print(f"❌ 下载失败 {ts_file} (尝试 {attempt + 1}/{max_retries}): {error_type}")

                if attempt == max_retries - 1:  # 最后一次尝试也失败
                    print(f"💥 放弃下载 {ts_file}，已达到最大重试次数")
                    return None

            except Exception as e:
                print(f"❌ 未知错误 {ts_file} (尝试 {attempt + 1}/{max_retries}): {e}")

                if attempt == max_retries - 1:
                    return None

        return None

    def _retry_failed_segments(self):
        """重试失败的片段下载"""
        print("🔄 开始重试失败的片段...")

        # 找出失败的片段
        downloaded_names = [f.name.replace('.ts.ts', '.ts') for f in self.ts_files]  # 修正文件名
        failed_segments = [ts for ts in self.ts_name_files if ts not in downloaded_names]

        print(f"🔄 需要重试 {len(failed_segments)} 个片段: {failed_segments}")

        max_retries = 3
        for retry_count in range(max_retries):
            print(f"🔄 重试第 {retry_count + 1}/{max_retries} 轮...")

            success_count = 0
            for ts_file in failed_segments[:]:  # 使用副本进行遍历
                print(f"🔄 重试下载: {ts_file}")
                result = self._download_ts_with_retry(ts_file, retry_count + 1)
                if result is not None:
                    self.ts_files.append(result)
                    failed_segments.remove(ts_file)
                    success_count += 1
                    # 重试成功一个后稍作延迟
                    time.sleep(random.uniform(0.5, 1.5))

            print(f"✅ 本轮重试成功 {success_count} 个片段")

            if not failed_segments:
                print("🎉 所有片段重试成功！")
                break

            # 如果还有失败的，等待一段时间再重试
            if retry_count < max_retries - 1 and failed_segments:
                wait_time = (retry_count + 1) * 2  # 等待时间递增
                print(f"⏳ 等待 {wait_time} 秒后进行下一轮重试...")
                time.sleep(wait_time)

        # 重试结束后重新排序
        self.ts_files.sort()

    # def _download_ts(self, ts_file):
    #     """下载单个TS文件"""
    #     ts_url = self.base_url + ts_file
    #     response = requests.get(ts_url, headers=self.headers)
    #
    #     if self.key:
    #         cipher = AES.new(self.key, AES.MODE_CBC, iv=b'\x00' * 16)
    #         decrypted = cipher.decrypt(response.content)
    #         # 简单填充处理
    #         if decrypted[-1] <= 16:
    #             decrypted = decrypted[:-decrypted[-1]]
    #     else:
    #         decrypted = response.content
    #
    #     filename = f"{ts_file}.ts"
    #     filepath = self.temp_dir / filename
    #     with open(filepath, 'wb') as f:
    #         f.write(decrypted)
    #     print(f"✅ 下载完成: {ts_file} ({len(decrypted)} bytes)✅")
    #     return filepath

    def _convert_to_mp4(self, input_ts, output_mp4):
        """使用ffmpeg将ts转换为mp4"""
        try:
            # 检查ffmpeg是否可用
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)

            # 转换命令
            cmd = [
                'ffmpeg', '-i', str(input_ts),
                '-c', 'copy',  # 直接复制流，不重新编码
                '-y',  # 覆盖输出文件
                str(output_mp4)
            ]

            subprocess.run(cmd, check=True, capture_output=False)
            return True

        except subprocess.CalledProcessError as e:
            print(f"ffmpeg转换失败: {e} ---> {output_mp4}")
            return False
        except FileNotFoundError:
            print("未找到ffmpeg，请先安装ffmpeg")
            return False

    def _cleanup(self, merged_ts):
        """清理临时文件"""
        for ts_file in self.ts_files:
            try:
                os.remove(ts_file)
            except Exception as e:
                print(f'_cleanup error ---------->{e}')
        try:
            if merged_ts.exists():
                os.remove(merged_ts)
            if self.temp_dir.exists():
                # 只删除空目录
                if not any(self.temp_dir.iterdir()):
                    os.rmdir(self.temp_dir)
        except Exception as e:
            print(f'_cleanup error ---------->{e}')


if __name__ == '__main__':
    downloader = ZMQM3U8Downloader("D:\\taolu\\爱开发的晖_93")
    downloader.set_download_url_dir("temp_dir", "https://zhuanma2.thysh.com/video/m3u5/1d56feec/index.m3u8", "out.mp4")
    downloader.start_download()
