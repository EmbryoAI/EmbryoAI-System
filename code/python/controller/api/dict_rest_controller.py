# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
from common import logger
import service.front.dict_service as dict_service
import time

dict_rest_controller = Blueprint('dict_rest_controller', __name__)
url_prefix = '/api/v1/dict'

#根据字典类别获取列表
@dict_rest_controller.route('/list/<string:dictClass>', methods=['GET'])
def queryDictListByClass(dictClass):
    logger().info('进入dict_rest_controller.queryDictListByClass查询字典列表')
    return dict_service.queryDictListByClass(dictClass)

#根据逗号隔开多个字典类别获取列表，减少ajax请求
@dict_rest_controller.route('/lists/<string:dictClass>', methods=['GET'])
def queryDictListByClassS(dictClass):
    logger().info('进入dict_rest_controller.queryDictListByClassS查询字典列表')
    return dict_service.queryDictListByClassS(dictClass)