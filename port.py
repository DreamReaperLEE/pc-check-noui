# *_*coding:utf-8 *_*
import json
import os
import re

import db
import web_test

# f = open("./port_config.txt")
# line = f.readline()
# while line:
#    print line,
#    line = f.readline()


# 该文件负责端口的信息查询及日志发送

# 获取端口列表黑名单
result = web_test.doPost('port_config', 'useless')
result = json.loads(result)
result = result['result']
port_list = []
for every in result:
    port_list.append(every.encode('utf-8'))


# 查询获取所有开放的非法端口信息并返回
def get_port_list():
    port_new = []
    endx = []
    # 查询所有的开放端口信息
    result = os.popen('netstat -an').readlines()
    # 逐行解析获取端口号
    for every in result:
        if 'TCP' in every:
            num = (re.findall(':[\d]* ', every))
            num = num[0]
            sourceport = num[1:-1]
            port_new.append(sourceport)
        if 'UDP' in every:
            num = (re.findall(':[\d]* ', every))
            num = num[0]
            sourceport = num[1:-1]
            port_new.append(sourceport)
    port_new = list(set(port_new))
    port_new = [x for x in port_new if x in port_list]
    for every in port_new:
        endx.append(int(every))
    endx.sort()
    return endx


# 将新旧端口列表进行比较，获得新开放的端口信息，并且生成日志
def update_port(old, new):
    if list(set(new).difference(set(old))):
        dif = list(set(new).difference(set(old)))
        for every in dif:
            every = str(every)
            data = {}
            data['level'] = '2'
            data['type'] = '设备事件'
            data['detail'] = '开放非法端口'
            data['msg'] = '非法开放端口号：' + every
            db.prt_error(data)
