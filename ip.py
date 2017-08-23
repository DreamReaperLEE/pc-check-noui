# *_*coding:utf-8 *_*
import json
import os
import re

import db
import sysname
import web_test

# 日志列表白名单，为内网IP段
ip_list = web_test.doPost('ip_config', 'useless')
ip_list = json.loads(ip_list)
ip_list = ip_list['result']
#获取本机建立的IP列表
def get_ip_list():
    ip_new = []
    result = os.popen('netstat -ano | findstr ESTABLISHED').readlines()
    #对获取到的IP信息进行逐行解析，得到IP及端口信息
    for a in result:
        num = (re.findall('\d [\s]*[\S]*:', a))
        x = num[0]
        x = x[1:(len(x) - 1)]
        x.strip()
        x = re.sub(' ', "", x)
        if x.startswith(tuple(ip_list)):
            continue
        ip_new.append(a)
    ip_new = list(set(ip_new))
    ip_new.sort()
    return ip_new


# 将新旧IP列表进行比较，获得新建立的IP连接信息，并且生成日志
def update_ip(old, new):
    #判断是否有新IP产生
    if list(set(new).difference(set(old))):
        result =' 主机名称：' + sysname.hostname
        out = result + ' TCP协议 '
        dif = list(set(new).difference(set(old)))
        for every in dif:
            num = (re.findall('[\d]*.[\d]*.[\d]*.[\d]*:[\d]*', every))
            sourceip = num[0]
            desip = num[1]
            temp = sourceip.split(":")
            sourceip = temp[0]
            sourceport = temp[1]
            temp = desip.split(":")
            desip = temp[0]
            desport = temp[1]
            every = out +'本机IP：'+ sourceip + ' 端口：' + sourceport + ' 目的IP：' + desip + ' 端口：' + desport
            data = {}
            data['level'] = '4'
            data['type'] = '设备事件'
            data['detail'] = '网络外联事件'
            data['msg'] = every
            db.prt_error(data)
