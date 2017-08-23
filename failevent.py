# *_*coding:utf-8 *_*
import os
import re
import socket
import win32evtlog

import db
import sysname


# 本文件负责用户登陆失败日志的分析

# 分析用户日志，并返回登陆失败信息，传入值为上次查询时的日志数量
def ReadLog(record_old):
    result = '主机名称：' + sysname.hostname + ' 主机IP：' + get_local_ip() + ' 登陆失败远端IP：' + get_remote_ip()
    computer = None
    # 查询的日志为系统Security日志
    logType = "Security"
    # 进行日志的读取
    h = win32evtlog.OpenEventLog(computer, logType)
    # 判断是否距离上次查询产生了新日志
    numRecords = win32evtlog.GetNumberOfEventLogRecords(h)
    new = numRecords - record_old
    # 循环读取新日志，直到全部日志解析完成
    while 1:
        objects = win32evtlog.ReadEventLog(h,
                                           win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ,
                                           0)
        if new == 0:
            break
        for object in objects:
            if new != 0:
                # 4525为Windows系统用户登陆失败日志ID
                if object.EventID == 4625:  # ==4625
                    temp = str(result)
                    temp = temp + str(object.TimeWritten) + ' ' + str(object.Sid)
                    data = {}
                    data['level'] = '1'
                    data['type'] = '用户事件'
                    data['detail'] = '登陆失败'
                    data['msg'] = temp
                    db.prt_error(data)
                new = new - 1
            else:
                break
    win32evtlog.CloseEventLog(h)
    return numRecords


# 查询系统Security日志下的日志数量
def Lognum():
    computer = None
    logType = "Security"
    h = win32evtlog.OpenEventLog(computer, logType)
    numRecords = win32evtlog.GetNumberOfEventLogRecords(h)
    return numRecords


# 获取本机IP
def get_local_ip():
    hostname = socket.gethostname()
    IPinfo = socket.gethostbyname_ex(hostname)
    LocalIP = IPinfo[2][2]
    return LocalIP


# 获取连入本机尝试登陆的机器IP，若没有则为localhost
def get_remote_ip():
    result = os.popen('netstat -an | findstr ":3389"').readline()
    if result:
        port = ':3389'
    else:
        result = os.popen('netstat -an | findstr ":22"').readline()
        port = ':22'
    if result:
        temp = result.split(port)
        result = temp[0]
        temp = (re.findall('[\d]*\.[\d]*\.[\d]*\.[\d]*', result))
        result = temp[1]
    else:
        result = 'localhost'
    return result
