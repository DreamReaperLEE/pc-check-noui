# *_*coding:utf-8 *_*
import os

# 获取本机名称，在程序开始时运行一次进行初始化
hostname = ''
result = os.popen('hostname').readline()
hostname = result[:-1]
