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

    days = current_date - contrast_date
    if str(days) == '0:00:00':
        days = 0
    else:
        days = int(str(days)[0:1])

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

