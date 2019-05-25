# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
import logUtils
from app import db
import service.admin.incubator_service as incubator_service
from entity.User import User
import time
from app import login_required 

incubator_rest_controller = Blueprint('incubator_rest_controller', __name__)
url_prefix = '/api/v1/incubator'

#新增培养箱
@incubator_rest_controller.route('/add', methods=['POST'])
@login_required
def addIncubator():
    logUtils.info('incubator_rest_controller.addIncubator-新增培养箱')
    code, incubator = incubator_service.insertIncubator(request)
    return make_response(jsonify(incubator), code)

 

#查询所有培养箱
@incubator_rest_controller.route('/list', methods=['GET'])
@login_required
def queryIncubatorList():
    logUtils.info('incubator_rest_controller.queryIncubatorList-查询所有培养箱')
    return incubator_service.queryIncubatorList(request)

#根据id删除培养箱
@incubator_rest_controller.route('/delete/<string:id>', methods=['GET'])
@login_required
def deleteIncubator(id):
    logUtils.info('incubator_rest_controller.deleteIncubator-根据id删除培养箱')
    incubator = incubator_service.findIncubatorById(id)
    if not incubator:
        abort(404)
    code, msg = incubator_service.deleteIncubator(id)
    return make_response(jsonify(msg), code)

#修改培养箱
@incubator_rest_controller.route('/update', methods=['POST'])
@login_required
def updateIncubator():
    logUtils.info('incubator_rest_controller.updateIncubator-修改培养箱')
    code, incubator = incubator_service.updateIncubator(request)
    return make_response(jsonify(incubator), code)

#根据皿ID获取培养箱编码
@incubator_rest_controller.route('/get/<string:dishId>', methods=['GET'])
def getIncubatorCodeByDishId(dishId):
    logUtils.info('incubator_rest_controller.getIncubatorCodeByDishId-根据皿ID获取培养箱编码')
    code, incubatorCode = incubator_service.getIncubatorCodeByDishId(dishId)
    return make_response(jsonify(incubatorCode), code)