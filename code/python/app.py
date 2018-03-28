#!/bin/env python
# -*- coding: utf8 -*-

from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from yaml import load

def read_yml_config(filename='configuration.yml'):
    '''从yaml文件中读取配置'''
    with open(filename, 'r') as fn:
        return load(fn.read())

def init_config(conf):
    '''初始化app的基本配置'''
    # 数据库连接字符串
    app.config['SQLALCHEMY_DATABASE_URI'] = conf['SQLALCHEMY_DATABASE_URI'] if \
        'SQLALCHEMY_DATABASE_URI' in conf else 'mysql+pymysql://root:@localhost/embryoai_system?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 返回的JSON数据保持原编码方式
    app.config['JSON_AS_ASCII'] = False

app = Flask(__name__) # EmbryoAI系统Flask APP
conf = read_yml_config()
init_config(conf)
db = SQLAlchemy(app) # 此APP要用到的数据库连接，由ORM框架SQLAlchemy管理
logger = app.logger # 日志对象

def init_logger():
    '''初始化日志的基本配置'''
    from logging.handlers import RotatingFileHandler
    handler = RotatingFileHandler('flasksql.log', maxBytes=1024*1024*200, backupCount=5)
    from logging import Formatter, DEBUG
    fmt = Formatter('%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    logger.setLevel(DEBUG)

def add_all_controller():
    ''' 在此方法中将所有controller蓝图注册到app中。
    例如：from controller.user_controller import user_controller
         app.register_blueprint(user_controller, url_prefix='/user')''' 
    pass

if __name__=='__main__':
    init_logger()
    port = conf['PORT'] if 'PORT' in conf else 5001 # app启动侦听的端口号
    debug = conf['DEBUG'] if 'DEBUG' in conf else False # 是否开启debug模式
    threaded = conf['THREADED'] if 'THREADED' in conf else True # 是否开启多线程模式
    app.run(port=port, debug=debug, threaded=threaded) #启动app