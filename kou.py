# *_*coding:utf-8 *_*

import db


# 该文件负责串口及并口的信息查询及日志发送

# 将新旧串口列表进行比较，若有串口占用或者释放，则生成日志
def update_serial(old, new):
    # 判断是否有串口被占用
    if list(set(new).difference(set(old))):
        dif = list(set(new).difference(set(old)))
        for every in dif:
            data = {}
            data['level'] = '2'
            data['type'] = '设备事件'
            data['detail'] = '串口占用'
            data['msg'] = '端口被占用：' + every
            db.prt_error(data)
    # 判断是否有串口被释放
    if list(set(old).difference(set(new))):
        dif = list(set(old).difference(set(new)))
        for every in dif:
            data = {}
            data['level'] = '1'
            data['type'] = '设备事件'
            data['detail'] = '串口释放'
            data['msg'] = '端口被释放：' + every
            db.prt_error(data)


# 将新旧并口列表进行比较，若有并口占用或者释放，则生成日志
def update_parallel(old, new):
    if list(set(new).difference(set(old))):
        dif = list(set(new).difference(set(old)))
        for every in dif:
            data = {}
            data['level'] = '2'
            data['type'] = '设备事件'
            data['detail'] = '并口占用'
            data['msg'] = '并口被占用：' + every
            db.prt_error(data)
    if list(set(old).difference(set(new))):
        dif = list(set(old).difference(set(new)))
        for every in dif:
            data = {}
            data['level'] = '1'
            data['type'] = '设备事件'
            data['detail'] = '并口释放'
            data['msg'] = '并口被释放：' + every
            db.prt_error(data)
