# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
from common import logger
from app import db
import service.front.procedure_service as procedure_service
from entity.User import User
import time

procedure_rest_controller = Blueprint('procedure_rest_controller', __name__)
url_prefix = '/api/v1/procedure'

#查询所有培养箱
@procedure_rest_controller.route('/list', methods=['GET'])
def queryProcedureList():
    logger().info('进入procedure_controller.procedure查询病历列表')
    return procedure_service.queryProcedureList(request)

#查询病历详情
@procedure_rest_controller.route('/<string:id>', methods=['GET'])
def procedureDetail(id):
    logger().info('进入procedure_controller.procedure查询病历详情')
    return procedure_service.getProcedureDetail(id)