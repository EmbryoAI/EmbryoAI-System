# -*- coding: utf8 -*-

from flask import Blueprint, make_response
from flask_restful import reqparse
import logUtils
import service.front.embryo_service as embryo_service
from app import login_required 

embryo_rest_controller = Blueprint('embryo_rest_controller', __name__)
url_prefix = '/api/v1/embryo'


#根据procedureId查询胚胎列表
@embryo_rest_controller.route('/list/<string:id>', methods=['GET'])
@login_required
def queryEmbryoList(id):
    logUtils.info('embryo_rest_controller.queryEmbryoList-根据procedureId查询胚胎列表')
    code, msg = embryo_service.queryEmbryoList(id)
    return make_response(msg, code)

#根据备胎ID标记当前备胎的结局
@embryo_rest_controller.route('/sign/<string:id>/<string:embryoFateId>', methods=['GET'])
@login_required
def signEmbryo(id,embryoFateId):
    logUtils.info('embryo_rest_controller.signEmbryo-根据备胎ID标记当前备胎的结局')
    code, msg = embryo_service.signEmbryo(id,embryoFateId)
    return make_response(msg, code)

#根据胚胎ID查询胚胎的相关信息
@embryo_rest_controller.route('/<string:id>', methods=['GET'])
@login_required
def getEmbryoById(id):
    logUtils.info('embryo_rest_controller.getEmbryoById-根据胚胎ID查询胚胎的相关信息')
    code, msg = embryo_service.getEmbryoById(id)
    return make_response(msg, code)

#根据胚胎ID查询患者相关信息
@embryo_rest_controller.route('/patient/<string:id>', methods=['GET'])
@login_required
def getPatientByEmbryoId(id):
    logUtils.info('embryo_rest_controller.getPatientByEmbryoId-根据胚胎ID查询患者相关信息')
    code, msg = embryo_service.getPatientByEmbryoId(id)
    return make_response(msg, code)

#根据皿读取ini文件获取胚胎数量
@embryo_rest_controller.route('/number', methods=['GET'])
def queryEmbryoNumber():
    logUtils.info('embryo_rest_controller.queryEmbryoNumber-根据皿读取ini文件获取胚胎数量')
    parser = reqparse.RequestParser()
    parser.add_argument('dishCode', type=str)
    code, msg = embryo_service.queryEmbryoNumber(parser.parse_args())
    return make_response(msg, code)