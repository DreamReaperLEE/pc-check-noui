# *_*coding:utf-8 *_*
import datetime
import threading
import time

# python d:python_workplace\pc-status-supervision\check-noui\end_Windows.pyw
import pythoncom
import wmi

import CDdriver
import USB
import User
import db
import failevent
import ip
import kou
import port
import sysinfo
import sysname
import web_test


# 轮询函数，进行状态的查询、日志生成等程序主要功能，将该函数放入线程中循环查询。
def query():
    # 初始化python的WMI链接
    pythoncom.CoInitialize()
    c = wmi.WMI()
    # 初始化失败用户列表
    logfail_old = failevent.Lognum()
    # 初始化系统信息列表
    sysinfo_old = []
    sysinfo_old = sysinfo_query(sysinfo_old)
    # 初始化User列表
    user_old = User.get_user_list()
    # 初始化USB列表
    temp = c.CIM_USBDevice()
    usb_old = []
    for interface in temp:
        st = interface.DeviceID.encode('utf-8')
        if 'VID_' in st:
            result = USB.query_usb(st)
            usb_old.append(result)
    # 初始化port列表
    port_old = []
    port_old = port_query(port_old)
    # 初始化ip列表
    ip_old = ip.get_ip_list()
    temp = []
    ip.update_ip(temp, ip_old)
    # 初始化serial列表
    temp = c.Win32_SerialPort()
    serial_old = []
    for interface in temp:
        st = interface.Description.encode('utf-8')
        serial_old.append(st)
    # 初始化parallel列表
    temp = c.Win32_ParallelPort()
    parallel_old = []
    for interface in temp:
        st = interface.Description.encode('utf-8')
        parallel_old.append(st)
    # 初始化CDdriver状态
    CDdriver_old = CDdriver.get_CDdriver_state()
    sysinfo_time = CDdriver_time = port_time = datetime.datetime.now()
    web_test.doSend('cdrom_exist', CDdriver.if_CDdriver_exist())
    # 循环查询进行状态更新及日志生成
    while 1:
        # 具体每个状态的更新由相应的状态名_query(传入旧列表)函数来负责，返回新列表并赋值给原来旧列表
        user_old = user_query(user_old)
        usb_old = usb_query(usb_old)
        # 判断是否距离上次时间过去1分钟，如果是则执行查询
        if (datetime.datetime.now() - datetime.timedelta(minutes=1)) > sysinfo_time:
            sysinfo_time = datetime.datetime.now()
            sysinfo_old = sysinfo_query(sysinfo_old)
        if (datetime.datetime.now() - datetime.timedelta(minutes=5)) > port_time:
            port_time = datetime.datetime.now()
            logfail_old = failevent.ReadLog(logfail_old)
            port_old = port_query(port_old)
        ip_old = ip_query(ip_old)
        serial_old = serial_query(serial_old)
        parallel_old = parallel_query(parallel_old)
        CDdriver_old = CDdriver_query(CDdriver_old)
        if (datetime.datetime.now() - datetime.timedelta(minutes=60)) > CDdriver_time:
            CDdriver_time = datetime.datetime.now()
            if CDdriver.if_CDdriver_exist() == 'yes':
                gtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                temp = '<2> ' + gtime + sysname.hostname + '26 DVD-ROM'
                web_test.doSend('cdrom_exist', '存在')
                data = {}
                data['level'] = '2'
                data['type'] = '设备事件'
                data['detail'] = '存在光驱设备'
                data['msg'] = temp
                db.prt_error(data)
        time.sleep(1)


# 查询用户状态并输出
def user_query(user_old):
    # 从User文件获取新的UserList
    user_new = User.get_user_list()
    # 将实时信息发送到代理服务器中
    web_test.doSend('user', user_new)
    # 进行新旧列表比较，若触发日志条件则发送日志。
    User.update_user(user_old, user_new)
    return user_new


# 查询系统状态并输出
def sysinfo_query(sysinfo_old):
    sysinfo_new = sysinfo.get_sys_info()
    web_test.doSend('sysinfo', sysinfo_new)
    return sysinfo_new


# 查询USB设备并输出状态
def usb_query(usb_old):
    # 初始化WMI连接
    pythoncom.CoInitialize()
    c = wmi.WMI()
    # 获取USB信息并解析
    temp = c.CIM_USBDevice()
    usb_new = []
    for interface in temp:
        st = interface.DeviceID.encode('utf-8')
        if 'VID_' in st:
            result = USB.query_usb(st)
            usb_new.append(result)
    web_test.doSend('usb', usb_new)
    USB.update_usb(usb_old, usb_new)
    return usb_new


# 查询端口并输出状态
def port_query(port_old):
    port_new = port.get_port_list()
    web_test.doSend('port', port_new)
    port.update_port(port_old, port_new)
    return port_new


# 查询ip并输出状态
def ip_query(ip_old):
    ip_new = ip.get_ip_list()
    web_test.doSend('ip', ip_new)
    ip.update_ip(ip_old, ip_new)
    return ip_new


# 查询Serial设备并输出状态
def serial_query(serial_old):
    pythoncom.CoInitialize()
    c = wmi.WMI()
    temp = c.Win32_SerialPort()
    serial_new = []
    for interface in temp:
        serial_new.append(interface.Description)
    web_test.doSend('serial', serial_new)
    kou.update_serial(serial_old, serial_new)
    return serial_new


# 查询Parallel设备并输出状态
def parallel_query(parallel_old):
    pythoncom.CoInitialize()
    c = wmi.WMI()
    temp = c.Win32_ParallelPort()
    parallel_new = []
    for interface in temp:
        parallel_new.append(interface.Description)
    web_test.doSend('parallel', parallel_new)
    kou.update_parallel(parallel_old, parallel_new)
    return parallel_new


# 查询CD并输出状态
def CDdriver_query(CDdriver_old):
    # 获取驱动器内介质信息
    CDdriver_new = CDdriver.get_CDdriver_state()
    # 获取当前时间
    gtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 判断是否是光驱挂载
    if CDdriver_new == 'yes' and CDdriver_old == 'no':
        temp = '<2> ' + gtime + sysname.hostname + ' 0 DVD-ROM'
        data = {}
        data['level'] = '2'
        data['type'] = '设备事件'
        data['detail'] = '光驱挂载'
        data['msg'] = temp
        db.prt_error(data)
    # 判断是否是光驱卸载
    if CDdriver_new == 'no' and CDdriver_old == 'yes':
        temp = '<3> ' + gtime + sysname.hostname + ' 1 DVD-ROM'
        data = {}
        data['level'] = '1'
        data['type'] = '设备事件'
        data['detail'] = '光驱卸载'
        data['msg'] = temp
        db.prt_error(temp)
    web_test.doSend('cdrom_state', CDdriver_new)
    return CDdriver_new


if __name__ == "__main__":
    # 创建线程，目标函数为query函数
    # 运行该脚本前请先运行代理服务器并保证网络通畅
    th = threading.Thread(target=query)
    th.start()
