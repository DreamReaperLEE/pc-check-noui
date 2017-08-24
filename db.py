# *_*coding:utf-8 *_*

import sysname
import web_test


# 根据VID以及PID向代理服务器查询USB设备的具体信息
def query_usb(vid, pid):
    data = {}
    data['vid'] = vid
    data['pid'] = pid
    usb = web_test.doPost('query_usb', data)
    return usb


# 向代理服务器输出日志信息
def prt_error(data):
    data['hostname'] = sysname.hostname
    web_test.doPost('prt_error', data)
