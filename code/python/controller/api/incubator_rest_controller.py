# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
from common import logger
from app import db
import service.admin.incubator_service as incubator_service
from entity.User import User
import time

incubator_rest_controller = Blueprint('incubator_rest_controller', __name__)
url_prefix = '/api/v1/incubator'

#新增培养箱
@incubator_rest_controller.route('/add', methods=['POST'])
def addIncubator():   
    code, incubator = incubator_service.insertIncubator(request)
    return make_response(jsonify(incubator), code)

 

#查询所有培养箱
@incubator_rest_controller.route('/list', methods=['GET'])
def queryIncubatorList():
    return incubator_service.queryIncubatorList(request)

#根据id删除培养箱
@incubator_rest_controller.route('/delete/<string:id>', methods=['GET'])
def deleteIncubator(id):
    incubator = incubator_service.findIncubatorById(id)
    if not incubator:
        abort(404)
    code, msg = incubator_service.deleteIncubator(id)
    return make_response(jsonify(msg), code)

#修改培养箱
@incubator_rest_controller.route('/update', methods=['POST'])
def updateIncubator():
    code, incubator = incubator_service.updateIncubator(request)
    return make_response(jsonify(incubator), code)