1. HttpCanary的安装、配置与使用

2. r0capture介绍
一个Hook抓包脚本，主要原理就是Hook了一些SSL相关的系统函数
GitHub地址 https://github.com/r0ysue/r0capture

3. r0capture的使用方式
先安装依赖 pip install hexdump
pip install frida
pip install frida-tools
attach模式，抓包内容可以保存成pcap文件供后续分析(包名找不到可能需要应用名称)
python r0capture.py -U com.qiyi.video -v -p iqiyi.pcap
spawn模式
python r0capture.py -U -f com.qiyi.video -v

4. WireShark
    如果保存成了pcap文件，可以使用这个工具来打开