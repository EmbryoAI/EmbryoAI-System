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

def parse_date(date_str):
    import time
    import datetime

    contrast_date = time.strptime(date_str,"%Y-%m-%d %H:%M:%S")
    current_date = datetime.datetime.now()
    days = int(current_date.day) - int(contrast_date[2])

    if days == 0:
        return days, '今天'
    if days == 1:
        return days, '昨天'
    if days == 2:
        return days, '前天'
    if days >= 3 and days <=7:
        return days, str(days) + '天前'
    if days > 7:
        return days, date_str
