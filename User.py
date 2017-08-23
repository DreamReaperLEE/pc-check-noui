# *_*coding:utf-8 *_*

import socket

import psutil

import db


# 该文件负责用户的登陆信息查询及日志发送

# 获取当前用户列表
def get_user_list():
    user_list = []
    users = psutil.users()
    for every in users:
        user_list.append(every[0])
    return user_list


# 获取本机IP
def get_local_ip():
    hostname = socket.gethostname()
    IPinfo = socket.gethostbyname_ex(hostname)
    LocalIP = IPinfo[2][2]
    return LocalIP


# 获取登陆的用户的远端IP
def get_remote_ip(user):
    users = psutil.users()
    for every in users:
        if every[0] == user:
            return every[2]
    return 'unknown'


# 将新旧用户列表进行比较，获得登入或登出的用户信息，并且生成日志
def update_user(old, new):
    if list(set(new).difference(set(old))):
        dif = list(set(new).difference(set(old)))
        for every in dif:
            every = '本机IP：' + get_local_ip() + ' 远端IP：' + get_remote_ip(every) + ' 用户名：' + every
            data = {}
            data['level'] = '1'
            data['type'] = '用户事件'
            data['detail'] = '登录成功'
            data['msg'] = every
            db.prt_error(data)
    if list(set(old).difference(set(new))):
        dif = list(set(old).difference(set(new)))
        for every in dif:
            every = '本机IP：' + get_local_ip() + ' 远端IP：' + get_remote_ip(every) + ' 用户名：' + every
            data = {}
            data['level'] = '1'
            data['type'] = '用户事件'
            data['detail'] = '退出登录'
            data['msg'] = every
            db.prt_error(data)
