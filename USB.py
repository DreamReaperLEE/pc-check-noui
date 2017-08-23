# *_*coding:utf-8 *_*

import db


# 该文件负责USB的信息查询及日志发送

# 查询所有的USB设备信息并返回
def query_usb(origin):
    usb_temp = origin.split("VID_")
    vid = usb_temp[1]
    vid = vid[:4]
    temp = origin.split("PID_")
    pid = temp[1]
    pid = pid[:4]
    # 将解析到的PID及VID在数据库中查询
    result = db.query_usb(vid, pid)
    return result


# 将新旧USB列表进行比较，获得插入或拔出的USB信息，并且生成日志
def update_usb(old, new):
    if list(set(new).difference(set(old))):
        dif = list(set(new).difference(set(old)))
        for every in dif:
            data = {}
            data['level'] = '2'
            data['type'] = '设备事件'
            data['detail'] = 'USB设备插入'
            data['msg'] = every
            db.prt_error(data)
    if list(set(old).difference(set(new))):
        dif = list(set(old).difference(set(new)))
        for every in dif:
            data = {}
            data['level'] = '1'
            data['type'] = '设备事件'
            data['detail'] = 'USB设备拔出'
            data['msg'] = every
            db.prt_error(data)
