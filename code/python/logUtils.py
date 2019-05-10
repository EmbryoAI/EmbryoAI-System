# -*- coding: utf8 -*-
import logging
from app import conf
from common import getdefault

def info(message):
  log(logging.INFO,message)

def error(message):
  log(logging.ERROR,message)

def debug(message):
  log(logging.DEBUG,message)

def warning(message):
  log(logging.WARNING,message)

def extra():
  orgId = getdefault(conf, 'ORG_ID', '123123') #读取医院ID
  extra = {
     "orgId":orgId
  }
  return extra

def log(type,message):
    from flask import current_app as app #获取全局日志对象
    if logging.ERROR==type: 
        app.logger.error(message,extra=extra())
    elif logging.INFO==type: 
        app.logger.info(message,extra=extra())
    elif logging.DEBUG==type: 
        app.logger.debug(message,extra=extra())
    else:
        app.logger.debug(message,extra=extra())