# -*- coding:utf-8 -*-
import os
from idaapi import plugin_t
from idaapi import PLUGIN_PROC
from idaapi import PLUGIN_OK
import ida_nalt
import idaapi
import idautils
import idc
import time


# 获取SO文件名和路径
def getSoPathAndName():
    fullpath = ida_nalt.get_input_file_path()
    filepath,filename = os.path.split(fullpath)
    return filepath,filename

# 获取代码段的范围
def getSegAddr():
    textStart = []
    textEnd = []

    for seg in idautils.Segments():
        if (idc.get_segm_name(seg)).lower() == '.text' or (
        idc.get_segm_name(seg)).lower() == 'text':
            tempStart = idc.get_segm_start(seg)
            tempEnd = idc.get_segm_end(seg)

            textStart.append(tempStart)
            textEnd.append(tempEnd)

    return min(textStart), max(textEnd)


class traceNatives(plugin_t):
    flags = PLUGIN_PROC
    comment = "traceNatives"
    help = ""
    wanted_name = "traceNatives"
    wanted_hotkey = ""

    def init(self):
        print("traceNatives(v0.1) plugin has been loaded.")
        return PLUGIN_OK

    def run(self, arg):
        # 查找需要的函数
        ea, ed = getSegAddr()
        search_result = []
        for func in idautils.Functions(ea, ed):
            try:
                functionName = str(idaapi.ida_funcs.get_func_name(func))
                if len(list(idautils.FuncItems(func))) > 10:
                    # 如果是thumb模式，地址+1
                    arm_or_thumb = idc.get_sreg(func, "T")
                    if arm_or_thumb:
                        func += 1
                    search_result.append(hex(func))
            except:
                pass

        so_path, so_name = getSoPathAndName()
        # 创建一个空列表，用来存放格式化后的结果
        formatted_list = []

        # 遍历原始列表中的每一个偏移量地址
        for offset in search_result:
            # 为每个偏移量生成格式化字符串，格式为：-a '库名!偏移量'
            #formatted_string = f"-a '{so_name}!{offset}'"
            formatted_string = "-a '" + so_name + '!' + offset + "'"
            # 将格式化好的字符串添加到新列表中
            formatted_list.append(formatted_string)

        # 用新的格式化列表替换原来的列表
        search_result = formatted_list

        #search_result = [f"-a '{so_name}!{offset}'" for offset in search_result]
        search_result = " ".join(search_result)

        script_name = so_name.split(".")[0] + "_" + str(int(time.time())) +".txt"
        save_path = os.path.join(so_path, script_name)
        with open(save_path, "w")as F:
            F.write(search_result)

        print("使用方法如下：")
        print("frida-trace -UF -O " + save_path)
        # print(f"frida-trace -UF -O {save_path}")

    def term(self):
        pass


def PLUGIN_ENTRY():
    return traceNatives()
