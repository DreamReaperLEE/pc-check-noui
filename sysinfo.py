# *_*coding:utf-8 *_*
import psutil

import db


# 该文件负责系统信息的查询及日志发送，有内存占用、CPU占用、盘符占用查询
# 查询内存占用、CPU占用、盘符占用并返回列表
def get_sys_info():
    # 内存占用率
    sys_info = []
    a = '当前内存占用率：' + (str)(psutil.virtual_memory().percent) + '%'
    sys_info.append(a)
    sysinfo_prt('内存利用率', a)
    # 本机cpu的总占用率
    a = ('当前cpu占用率： ' + (str)(psutil.cpu_percent()) + '%')
    sys_info.append(a)
    sysinfo_prt('CPU利用率', a)
    # 本机磁盘的总占用率
    for i in psutil.disk_partitions():
        if i[2] == 'NTFS':
            a = ("盘符:" + i[0] + '使用率:' + str(psutil.disk_usage(i[1])[3])) + '%'
            sys_info.append(a)
            sysinfo_prt('硬盘利用率', a)
    return sys_info


# 将信息生成日志存入数据库
def sysinfo_prt(detail, msg):
    data = {}
    data['level'] = '0'
    data['type'] = '实时状态'
    data['detail'] = detail
    data['msg'] = msg
    db.prt_error(data)
