# *_*coding:utf-8 *_*
import json
import logging
import logging.handlers
import urllib
import urllib2


# 该函数决定采用那种方式向服务器传值
def doSend(name, msg):
    result = doPost(name, msg)
    return result


# 采用get方法向代理服务器传送实时信息
def doGet(name, msg):
    url = 'http://127.0.0.1:8000/update'
    msg = json.dumps(msg)
    textmod = {'name': name, 'msg': msg}
    textmod = urllib.urlencode(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    res = res.read()
    return res


# 采用Syslog向采集器传送信息（未采用本服务，如果需要，则在本文件的dosend函数中增加该函数调用即可）
def doLog(msg):
    logger = logging.getLogger()
    fh = logging.handlers.SysLogHandler(('127.0.0.1', 514), logging.handlers.SysLogHandler.LOG_AUTH)
    # gtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.warning("msg")
    logger.error("msg")


# 采用Post方式向代理服务器传值，传值为json格式
def doPost(name, msg):
    data = {}
    data['name'] = name
    data['msg'] = msg
    data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url='http://127.0.0.1:8000/get_json', headers=headers, data=data)
    response = urllib2.urlopen(request)
    response=response.read()
    return response