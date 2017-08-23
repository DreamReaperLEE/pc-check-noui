# *_*coding:utf-8 *_*
import os

import re


# 该文件为驱动器状态查询文件

# 该函数负责查询驱动器内是否有介质
def get_CDdriver_state():
    # 模拟命令行获取磁盘信息
    val = os.popen('ECHO LIST VOLUME|DISKPART').readlines()
    ROM_new = 'no'
    # 逐行解析信息，找寻驱动器的相关信息
    for line in val:
        if re.search('ROM', line):
            if re.search('0 B', line):
                ROM_new = '无介质'
            else:
                ROM_new = '存在介质'

    return ROM_new


# 该函数负责查询驱动器是否存在于电脑内
def if_CDdriver_exist():
    # 模拟命令行获取磁盘信息
    val = os.popen('ECHO LIST VOLUME|DISKPART').readlines()
    print val
    exist = 'no'
    for line in val:
        print line
        if re.search('ROM', line):
            exist = 'yes'
    return exist
