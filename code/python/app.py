#!/bin/env python
# -*- coding: utf8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from yaml import load
from traceback import print_exc
from common import getdefault
from logging import Formatter, DEBUG
import os

from flask_apscheduler import APScheduler

app_root = os.path.split(os.path.realpath(__file__))[0] + os.path.sep

def read_yml_config( filename=app_root + 'configuration.yml'):
    '''从yaml文件中读取配置'''
    with open(filename, 'r') as fn:
        return load(fn.read())        

def init_config(conf):
    '''初始化app的基本配置'''
    # 数据库连接字符串
    app.config['SQLALCHEMY_DATABASE_URI'] = getdefault(conf, 'SQLALCHEMY_DATABASE_URI', 
        'mysql+pymysql://root:123456@localhost/embryoai_system?charset=utf8')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SCHEDULER_API_ENABLED'] = getdefault(conf, 'SCHEDULER_API_ENABLED', True)
    app.config['JOBS'] = getdefault(conf, 'JOBS')
    # 返回的JSON数据保持原编码方式
    app.config['JSON_AS_ASCII'] = False
    app.config['SECRET_KEY'] = getdefault(conf, 'SECRET_KEY', '123456')

app = Flask(__name__) # EmbryoAI系统Flask APP
conf = read_yml_config()
init_config(conf)
db = SQLAlchemy(app) # 此APP要用到的数据库连接，由ORM框架SQLAlchemy管理
logger = app.logger # 日志对象

def init_logger(logname):
    '''初始化日志的基本配置'''
    global logger
    path, _ = os.path.split(logname)
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except Exception:
            print_exc()
            logname = 'embryoai.log'
    from logging.handlers import RotatingFileHandler
    handler = RotatingFileHandler(logname, maxBytes=1024*1024*200, backupCount=5)
    fmt = Formatter('%(asctime)s [%(filename)s (%(funcName)s) '
        ': Line %(lineno)d] %(levelname)s: %(message)s')
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    logger.setLevel(DEBUG)

def add_all_controller():
    ''' 在此方法中将所有controller蓝图注册到app中。
        controller中定义的Blueprint的变量名称必须与文件名称相同，
        可以定义url_prefix变量设置controller的url前缀''' 
    from importlib import import_module
    global app_root
    for root, _, files in os.walk(app_root + 'controller'):
        for f in filter(lambda x: x.endswith('.py') 
            and not x.startswith('__init__'), files):
            f = f[:-3]
            root = root[len(app_root):]
            path = list(filter(lambda x: x!='', root.split(os.path.sep)))
            path.append(f)
            modulename = '.'.join(path)
            controller_module = import_module(modulename)
            controller_variable = getattr(controller_module, f)
            prefix_variable = getattr(controller_module, 'url_prefix', '/')
            # setattr(controller_variable, 'template_folder', 'templates')
            app.register_blueprint(controller_variable, url_prefix=prefix_variable)
            logger.info('控制器 %s 蓝图注册成功，绑定地址前缀 %s' %(
                controller_variable.name, prefix_variable))

if __name__=='__main__':
    init_logger(getdefault(conf, 'LOGGER_FILE', 'embryoai.log'))
    port = getdefault(conf, 'PORT', 5001) # app启动侦听的端口号
    debug = getdefault(conf, 'DEBUG', False) # 是否开启debug模式
    threaded = getdefault(conf, 'THREADED', True) # 是否开启多线程模式
    add_all_controller()
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    logger.info('服务器启动成功，侦听端口：%d' %port)
    app.run(port=port, debug=debug, threaded=threaded, use_reloader=False) #启动app
