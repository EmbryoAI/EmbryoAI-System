# -*- coding: utf8 -*-

from flask import Blueprint,make_response
from flask_restful import reqparse
from common import logger
import service.front.well_service as well_service
from app import login_required 


well_rest_controller = Blueprint('well_rest_controller', __name__)
url_prefix = '/api/v1/well'


#根据procedureId,dishCode获取孔列表
@well_rest_controller.route('/list/<string:procedureId>/<string:dishId>', methods=['GET'])
@login_required
def queryWellList(procedureId, dishId):
    return well_service.queryWellList(procedureId, dishId)

#根据路径返回孔缩略图
@well_rest_controller.route('/image', methods=['GET'])
@login_required
def getWellImage():
    parser = reqparse.RequestParser()
    parser.add_argument('image_path', type=str)
    return well_service.getWellImage(parser.parse_args())

#根据当前时间序列获取上一帧序列
@well_rest_controller.route('/preframe', methods=['GET'])
@login_required
def getPreFrame():
    parser = reqparse.RequestParser()
    parser.add_argument('current_seris', type=str)
    return well_service.getPreFrame(parser.parse_args())

#根据当前时间序列获取下一帧序列
@well_rest_controller.route('/nextframe', methods=['GET'])
@login_required
def getNextFrame():
    parser = reqparse.RequestParser()
    parser.add_argument('current_seris', type=str)
    return well_service.getNextFrame(parser.parse_args())