# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
from common import logger
from app import db
import service.front.procedure_service as procedure_service
from entity.User import User
import time
from app import login_required 

procedure_rest_controller = Blueprint('procedure_rest_controller', __name__)
url_prefix = '/api/v1/procedure'

#查询所有培养箱
@procedure_rest_controller.route('/list', methods=['GET'])
@login_required
def queryProcedureList():
    logger().info('进入procedure_controller.procedure查询病历列表')
    return procedure_service.queryProcedureList(request)

#查询病历详情
@procedure_rest_controller.route('/<string:id>', methods=['GET'])
@login_required
def procedureDetail(id):
    return procedure_service.getProcedureDetail(id)

#修改病历信息(仅限修改电话,邮箱,地址,周期备注)
@procedure_rest_controller.route('/info', methods=['POST'])
@login_required
def updateProcedure():
    code, msg = procedure_service.updateProcedure(request)
    return make_response(msg, code)

#查询根据输入值补全病历号
@procedure_rest_controller.route('/no/list', methods=['GET'])
@login_required
def queryMedicalRecordNoList():
    logger().info('进入procedure_controller.queryMedicalRecordNoList')
    return procedure_service.queryMedicalRecordNoList(request)

#根据id删除病历
@procedure_rest_controller.route('/delete/<string:id>', methods=['GET'])
@login_required
def deleteProcedure(id):
    procedure = procedure_service.getProcedureDetail(id)
    if not procedure:
        abort(404)
    code, msg = procedure_service.deleteProcedure(id)
    return make_response(jsonify(msg), code)

#新建病历
@procedure_rest_controller.route('/add', methods=['POST'])
@login_required
def add():
    code, msg = procedure_service.addProcedure(request)
    return make_response(jsonify(msg), code)