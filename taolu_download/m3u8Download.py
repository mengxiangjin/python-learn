import os
import time
from pickle import GLOBAL

import requests
import m3u8
from pathlib import Path
from urllib.parse import urljoin
from tqdm import tqdm
import subprocess
import concurrent.futures

download_result_flag = True

headers =  {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'Referer': 'http://MAfAIOo0E8EMOWPA.black'
        }

class M3U8Downloader:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = None

    def set_temp_dir(self, temp_dir_name):
        """设置临时目录"""
        self.temp_dir = self.output_dir / temp_dir_name
        self.temp_dir.mkdir(exist_ok=True)
        return self.temp_dir

    def download_m3u8_to_mp4(self, m3u8_url, output_filename=None):
        """
        下载m3u8并转换为mp4

        Args:
            m3u8_url: m3u8文件URL
            output_filename: 输出文件名
        """
        global download_result_flag
        download_result_flag = True

        try:
            # 1. 解析m3u8文件
            print("正在解析m3u8文件...")
            segments = self._parse_m3u8(m3u8_url)

            if not segments:
                print("未找到视频片段")
                return False

            # 2. 下载所有ts片段
            print(f"开始下载 {len(segments)} 个视频片段...")
            ts_files = self._download_segments(segments, m3u8_url)

            # if not download_result_flag:
            #     print(f"已达到最大重试次数，请重试: {m3u8_url}")
            #     return False

            # 3. 合并ts文件
            print("正在合并视频片段...")
            merged_ts = self._merge_segments(ts_files)

            # 4. 转换为mp4
            print("正在转换为mp4...")
            if output_filename is None:
                output_filename = "output.mp4"
            elif not output_filename.endswith('.mp4'):
                output_filename += '.mp4'

            output_path = self.output_dir / output_filename
            self._convert_to_mp4(merged_ts, output_path)

            # 5. 清理临时文件
            self._cleanup(ts_files, merged_ts)

            print(f"转换完成: {output_path}")
            return True

        except Exception as e:
            print(f"处理失败: {e}")
            return False

    def _parse_m3u8(self, m3u8_url):
        """解析m3u8文件，获取所有ts片段URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
                'Referer': 'http://MAfAIOo0E8EMOWPA.black'
            }
            response = requests.get(m3u8_url, headers=headers,timeout=10)
            response.raise_for_status()

            # 解析m3u8内容
            playlist = m3u8.loads(response.text)

            # 获取所有ts片段的URI
            segments = []
            for segment in playlist.segments:
                segment_url = urljoin(m3u8_url, segment.uri)
                segments.append(segment_url)

            return segments

        except Exception as e:
            print(f"解析m3u8失败: {e}")
            return []

    def _download_segment(self, segment_url, index):
        """下载单个ts片段"""
        try:
            # if download_result_flag is False:
            #     return None
            response = requests.get(segment_url, timeout=30,headers=headers)
            response.raise_for_status()

            filename = f"segment_{index:04d}.ts"
            filepath = self.temp_dir / filename

            with open(filepath, 'wb') as f:
                f.write(response.content)

            return filepath

        except Exception as e:
            print(f"下载片段 {index} 失败: {e}")
            return None

    def _download_segments(self, segments, base_url, max_retries=3):
        """多线程下载所有ts片段，支持重试机制"""
        ts_files = []

        def download_with_retry(segment, index, retry_count=0):
            """带重试的下载函数"""
            try:
                result = self._download_segment(segment, index)
                if result is None:
                    if retry_count < max_retries:
                        print(f"片段 {index} 第 {retry_count + 1} 次重试...")
                        time.sleep(1 * (retry_count + 1))
                        return download_with_retry(segment, index, retry_count + 1)
                    else:
                        global download_result_flag
                        download_result_flag = False

                        raise Exception(f"片段 {index} 下载失败，已达最大重试次数")
                return result  # 重要：返回下载结果

            except Exception as e:
                if retry_count < max_retries:
                    print(f"片段 {index} 第 {retry_count + 1} 次重试... 错误: {e}")
                    time.sleep(1 * (retry_count + 1))
                    return download_with_retry(segment, index, retry_count + 1)
                else:
                    download_result_flag = False

                    raise Exception(f"片段 {index} 下载失败，已达最大重试次数: {e}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # 创建下载任务（带重试）
            future_to_index = {
                executor.submit(download_with_retry, segment, i): i
                for i, segment in enumerate(segments)
            }

            # 显示进度
            with tqdm(total=len(segments), desc="下载进度") as pbar:
                for future in concurrent.futures.as_completed(future_to_index):
                    index = future_to_index[future]
                    try:
                        result = future.result()
                        if result:
                            ts_files.append(result)
                    except Exception as e:
                        print(f"片段 {index} 最终下载失败: {e}")
                    finally:
                        pbar.update(1)

        # 按索引顺序排序
        ts_files.sort()
        return ts_files
    def _merge_segments(self, ts_files):
        """合并所有ts文件为一个文件"""
        merged_file = self.temp_dir / "merged.ts"

        with open(merged_file, 'wb') as outfile:
            for ts_file in tqdm(ts_files, desc="合并进度"):
                with open(ts_file, 'rb') as infile:
                    outfile.write(infile.read())

        return merged_file

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

    def _cleanup(self, ts_files, merged_ts):
        """清理临时文件"""
        for ts_file in ts_files:
            try:
                os.remove(ts_file)
            except Exception as e:
                print(f'_cleanup error ---------->{e}')
        try:
            os.remove(merged_ts)
            os.rmdir(self.temp_dir)
        except:
            print(f'_cleanup error ---------->')


# 使用示例
if __name__ == "__main__":
    pass