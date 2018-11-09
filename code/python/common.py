# -*- coding: utf8 -*-
import numpy as np
import cv2


def cross_domain(func):
    '''实现跨域访问装饰器，在每个需要实现跨域访问的controller方法前加标签 @cross_domain 即可
       例如：
       @controller.route('/', methods=['GET'])
       @cross_domain
       def getUser():
           # ......
    '''
    from functools import wraps
    from flask import make_response
    @wraps(func)
    def allow_origin(*args, **kwargs):
        response = make_response(func(*args, **kwargs))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Referer,Accept,Origin,User-Agent'
        return response
    return allow_origin

def getdefault(d, key, defaultValue=None):
    '''获取字典值，当key不存在时，不会抛出异常，而是返回默认值'''
    from collections import namedtuple
    if not isinstance(d, dict) and not isinstance(d, namedtuple):
        raise TypeError('参数 %s 不是一个key-value对象' %d)
    return d[key] if key in d else defaultValue

def logger():
    '''获取全局日志对象'''
    from flask import current_app as app
    return app.logger

def uuid():
    '''获取一个UUID值'''
    import uuid
    return str(uuid.uuid1()).replace('-', '')

#时间格式转换方法 date_str:需要转换的时间字符串 type:精确位置 0:精确到秒  1:精确到分
def parse_date(date_str, type):
    import time
    import datetime

    contrast_date = time.strptime(date_str,"%Y-%m-%d %H:%M:%S")
    contrast_date = datetime.date(contrast_date[0], contrast_date[1], contrast_date[2])
    current_date = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
    d1 = datetime.datetime.strptime(str(current_date), '%Y-%m-%d')
    d2 = datetime.datetime.strptime(str(contrast_date), '%Y-%m-%d')
    days = (d1 - d2).days

    if days == 0:
        return '今天'
    if days == 1:
        return '昨天'
    if days == 2:
        return '前天'
    if days >= 3 and days <=7:
        return str(days) + '天前'
    if days > 7 and type == 0:
        return date_str
    if days > 7 and type == 1:
        return time.strftime("%Y-%m-%d %H:%M", time.strptime(date_str, "%Y-%m-%d %H:%M:%S"))  

def nested_dict(obj):
    if not hasattr(obj,"__dict__"):
        return obj
    result = {}
    for key, val in obj.__dict__.items():
        if key.startswith("_"):
            continue
        element = []
        if isinstance(val, list):
            for item in val:
                element.append(nested_dict(item))
        elif isinstance(val, dict):
            element = {}
            for child_key in val:
                element[child_key] = nested_dict(val[child_key])
        else:
            element = nested_dict(val)
        result[key] = element
    return result

def parse_time_for_date_str(date):
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    hour = date[8:10]
    min = date[10:12]
    return year + "-" + month + "-" + day + " " + hour + ":" + min

def get_serie_time(insemi_time, cap_start_time, time_serie):
    ''' 获得某一个采集时间序列距离授精时间的时间间隔 
        @param insemi_time: 授精时间字符串，格式"%Y-%m-%d %H:%M"
        @param cap_start_time: 开始采集时间字符串，可以为格式"%Y-%m-%d %H:%M"或采集目录名称格式
        @param time_serie: 时间序列字符串，7位数字组成，与时间序列目录名称一致
        @returns hour, minute 该时间序列距离授精时间的小时和分钟数
    '''
    import datetime as dt
    from task.TimeSeries import serie_to_minute
    if len(insemi_time) == 16:
        in_time = dt.datetime.strptime(insemi_time, '%Y-%m-%d %H:%M')
    elif len(insemi_time) == 19:
        in_time = dt.datetime.strptime(insemi_time, '%Y-%m-%d %H:%M:%S')
    else:
        raise ValueError('授精时间字符串格式错误')
    if len(cap_start_time) == 16:
        cap_time = dt.datetime.strptime(cap_start_time, '%Y-%m-%d %H:%M')
    elif len(cap_start_time) == 19:
        cap_time = dt.datetime.strptime(cap_start_time, '%Y-%m-%d %H:%M:%S')
    elif len(cap_start_time) == 14:
        cap_time = dt.datetime.strptime(cap_start_time, '%Y%m%d%H%M%S')
    else:
        raise ValueError('开始采集时间字符串格式错误')
    ts_minutes = serie_to_minute(time_serie)
    cap_minutes = (cap_time - in_time).total_seconds()//60
    return divmod(cap_minutes + ts_minutes, 60)

def get_serie_time_hours(insemi_time, cap_start_time, time_serie):
    ''' 获得某一个采集时间序列距离授精时间的小时数（取整）间隔 
        @param insemi_time: 授精时间字符串，格式"%Y-%m-%d %H:%M"
        @param cap_start_time: 开始采集时间字符串，可以为格式"%Y-%m-%d %H:%M"或采集目录名称格式
        @param time_serie: 时间序列字符串，7位数字组成，与时间序列目录名称一致
        @returns hours 该时间序列距离授精时间的小时数
    '''
    h, m = get_serie_time(insemi_time, cap_start_time, time_serie)
    return h + m/60

''' 获得某一个采集时间序列距离授精时间的分钟数间隔的匿名函数 '''
get_serie_time_minutes = lambda insemi_time, cap_start_time, time_serie: (
    get_serie_time_hours(insemi_time, cap_start_time, time_serie) * 60
) 

import unittest
class CommonTest(unittest.TestCase):
    def test(self):
        d1 = '2018-09-11 12:30'
        d2 = '2018-09-11 15:00'
        ts = '2101500'
        self.assertEqual(get_serie_time(d1, d2, ts), (60, 45))
        self.assertEqual(get_serie_time_hours(d1, d2, ts), 60.75)
        self.assertEqual(get_serie_time_minutes(d1, d2, ts), 3645)
        d2 = '20180911150000'
        self.assertEqual(get_serie_time(d1, d2, ts), (60, 45))
        d1 = '2018-11-01 14:50:00'
        d2 = '2018-11-01 18:35:00'
        ts = '6224500'
        self.assertEqual(get_serie_time(d1, d2, ts), (170, 30))     
        self.assertEqual(get_serie_time_hours(d1, d2, ts), 170.5)
        self.assertEqual(get_serie_time_minutes(d1, d2, ts), 10230)   

if __name__=='__main__':
    unittest.main()
    

    
