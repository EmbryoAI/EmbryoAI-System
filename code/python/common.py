# -*- coding: utf8 -*-

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
        rst.headers['Access-Control-Allow-Headers'] = 'Referer,Accept,Origin,User-Agent'
        return response
    return allow_origin
