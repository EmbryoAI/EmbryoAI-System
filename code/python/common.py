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

def image_sharpness(img, mode='BGR'):
    '''求图像清晰度度量值
    img - numpy array代表的图像
    mode - BGR/RGB/RGBA/GRAY
    '''
    if not isinstance(img, np.ndarray):
        raise TypeError('参数不是一个numpy张量')
    if img.ndim < 2 or img.ndim > 3:
        raise TypeError('参数numpy张量不是一张图像')
    if img.ndim == 3 and img.shape[2] not in (3, 4):
        raise ValueError('图像参数数据错误，非RGB图像或RGBA图像')
    if img.ndim == 3:
        if mode == 'BGR':
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = img.astype(np.int64)
    diff_x = np.abs(img[1:,:] - img[:-1,:])
    diff_y = np.abs(img[:,1:] - img[:,:-1])
    return diff_x.mean() + diff_y.mean()

def uuid():
    '''获取一个UUID值'''
    import uuid
    return str(uuid.uuid1()).replace('-', '')

