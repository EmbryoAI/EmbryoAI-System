#!/bin/env python
# -*- coding: utf-8 -*-

from traceback import print_exc
from logging import Formatter
import logging
import os
import sys

# from flask import Flask
import sentry_sdk  # sentry.io SDK 导入
from sentry_sdk.integrations.flask import Flask, FlaskIntegration  # sentry.io Flask 集成
from sentry_sdk.integrations.sqlalchemy import (
    SqlalchemyIntegration,
)  # sentry.io SQLAlchemy 集成
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from yaml import load
from keras.models import load_model
import logstash  # LOGSTASH日志采集 add liuyz 20190505

# 使用在common中初始化的scheduler  liuyz---为了解决定时任务无法获取上下文
from common import getdefault, scheduler

# from flask_apscheduler import APScheduler   屏蔽该行，已经在common中初始化  liuyz---为了解决定时任务无法获取上下文
import logUtils

# from minio import Minio
# from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
#                          BucketAlreadyExists)

app_root = os.path.dirname(__file__) + os.path.sep
minioClient = None
organizationId = None


def read_yml_config(filename=app_root + "configuration.yml", env="dev"):
    """从yaml文件中读取配置"""
    with open(filename, "rb") as fn:
        return load(fn.read())[env]


def init_config(conf):
    """初始化app的基本配置"""
    from datetime import timedelta

    # 数据库连接字符串
    app.config["SQLALCHEMY_DATABASE_URI"] = getdefault(
        conf,
        "SQLALCHEMY_DATABASE_URI",
        "mysql+pymysql://root:123456@localhost/embryoai_system?charset=utf8",
    )
    app.config["SQLALCHEMY_POOL_RECYCLE"] = getdefault(
        conf, "SQLALCHEMY_POOL_RECYCLE", 3
    )
    app.config["SQLALCHEMY_POOL_SIZE"] = getdefault(conf, "SQLALCHEMY_POOL_SIZE", 10)
    app.config["SQLALCHEMY_POOL_TIMEOUT"] = getdefault(
        conf, "SQLALCHEMY_POOL_TIMEOUT", 3
    )
    app.config["SQLALCHEMY_MAX_OVERFLOW"] = getdefault(
        conf, "SQLALCHEMY_MAX_OVERFLOW", 500
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SCHEDULER_API_ENABLED"] = getdefault(
        conf, "SCHEDULER_API_ENABLED", True
    )
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(
        seconds=getdefault(conf, "SEND_FILE_MAX_AGE_DEFAULT", 60)
    )
    app.config["JOBS"] = getdefault(conf, "JOBS")
    app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = getdefault(
        conf, "SQLALCHEMY_COMMIT_ON_TEARDOWN", True
    )
    # 返回的JSON数据保持原编码方式
    app.config["JSON_AS_ASCII"] = False
    app.config["SECRET_KEY"] = getdefault(conf, "SECRET_KEY", "123456")


app = Flask(__name__)  # EmbryoAI系统Flask APP
if len(sys.argv) < 2 or sys.argv[-1] == "dev" or sys.argv[-1] not in ("stage", "prod"):
    conf = read_yml_config()
    conf["EMBRYOAI_IMAGE_ROOT"] = (
        app_root + ".." + os.path.sep + "captures" + os.path.sep
    )
else:
    conf = read_yml_config(env=sys.argv[-1])

# sentry.io SDK 初始化，将所有错误异常保存到sentry.io
sentry_sdk.init(
    dsn=conf["SENTRY_DSN"], integrations=[FlaskIntegration(), SqlalchemyIntegration()]
)

init_config(conf)
db = SQLAlchemy(app)  # 此APP要用到的数据库连接，由ORM框架SQLAlchemy管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login_controller.index"
logger = app.logger


@app.teardown_request
def shutdown_session(exc=None):
    if app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"]:
        if exc is None:
            db.session.commit()
    elif exc:
        db.session.rollback()
    db.session.remove()


# @app.after_request
# def shutdown_session(response):
#     db.session.remove()
#     return response


@login_manager.user_loader
def load_user(user_id):
    import service.admin.user_service as user_service

    return user_service.findUserById(user_id)


def init_logger(logname):
    """初始化日志的基本配置"""
    global logger
    path, _ = os.path.split(logname)
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except Exception:
            print_exc()
            logname = "embryoai.log"
    from logging.handlers import RotatingFileHandler

    handler = RotatingFileHandler(logname, maxBytes=1024 * 1024 * 200, backupCount=5)
    fmt = Formatter(
        "%(asctime)s [%(filename)s (%(funcName)s) "
        ": Line %(lineno)d] %(levelname)s: %(message)s"
    )
    ch = logging.StreamHandler()  # 输出控制台Handler liuyz add 20190506
    ch.setFormatter(fmt)
    handler.setFormatter(fmt)
    logger.addHandler(ch)
    logger.addHandler(handler)

    level = getdefault(conf, "LOGGER_LEVEL", "DEBUG")
    logger.setLevel(level)

    # LOGSTASH日志采集 add liuyz 20190505
    LOGSTASH_HOST = getdefault(conf, "LOGSTASH_HOST", "39.104.173.18")
    LOGSTASH_PORT = getdefault(conf, "LOGSTASH_PORT", "5066")
    logger.addHandler(
        logstash.TCPLogstashHandler(LOGSTASH_HOST, LOGSTASH_PORT, version=1)
    )


def add_all_controller():
    """ 在此方法中将所有controller蓝图注册到app中。
        controller中定义的Blueprint的变量名称必须与文件名称相同，
        可以定义url_prefix变量设置controller的url前缀"""
    from importlib import import_module

    global app_root
    for root, _, files in os.walk(app_root + "controller"):
        for f in filter(
            lambda x: x.endswith(".py") and not x.startswith("__init__"), files
        ):
            f = f[:-3]
            root_dir = root[len(app_root) :]
            path = list(filter(lambda x: x != "", root_dir.split(os.path.sep)))
            path.append(f)
            modulename = ".".join(path)
            controller_module = import_module(modulename)
            controller_variable = getattr(controller_module, f)
            prefix_variable = getattr(controller_module, "url_prefix", "/")
            # setattr(controller_variable, 'template_folder', 'templates')
            app.register_blueprint(controller_variable, url_prefix=prefix_variable)
            logger.info(
                "控制器 %s 蓝图注册成功，绑定地址前缀 %s" % (controller_variable.name, prefix_variable),
                extra=logUtils.extra(),
            )


model_file = getdefault(conf, "KERAS_MODEL_NAME", "embryo_model.h5")
model = load_model(app_root + "cv" + os.path.sep + model_file)
model._make_predict_function()

if __name__ == "__main__":
    init_logger(getdefault(conf, "LOGGER_FILE", "embryoai.log"))
    port = getdefault(conf, "PORT", 5001)  # app启动侦听的端口号
    debug = getdefault(conf, "DEBUG", False)  # 是否开启debug模式
    threaded = getdefault(conf, "THREADED", True)  # 是否开启多线程模式
    add_all_controller()
    #     scheduler = APScheduler()
    scheduler.init_app(app)  # 使用common中初始化好的scheduler---为了定时任务获取到上下文
    scheduler.start()
    logger.info("服务器启动成功，侦听端口：%d" % port, extra=logUtils.extra())
    app.run(
        port=port, debug=debug, threaded=threaded, use_reloader=False, host="0.0.0.0"
    )  # 启动app
