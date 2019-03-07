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
    code, msg = well_service.queryWellList(procedureId, dishId)
    return make_response(msg, code)

#根据路径返回孔缩略图
@well_rest_controller.route('/image', methods=['GET'])
@login_required
def getWellImage():
    parser = reqparse.RequestParser()
    parser.add_argument('image_path', type=str)
    code, msg = well_service.getWellImage(parser.parse_args())
    return make_response(msg, code)

#根据当前时间序列获取上一帧序列
@well_rest_controller.route('/preframe', methods=['GET'])
@login_required
def getPreFrame():
    parser = reqparse.RequestParser()
    parser.add_argument('current_seris', type=str)
    code, msg = well_service.getPreFrame(parser.parse_args())
    return make_response(msg, code)

#根据当前时间序列获取下一帧序列
@well_rest_controller.route('/nextframe', methods=['GET'])
@login_required
def getNextFrame():
    parser = reqparse.RequestParser()
    parser.add_argument('current_seris', type=str)
    code, msg = well_service.getNextFrame(parser.parse_args())
    return make_response(msg, code)

#将孔下面的所有大图生成视频
@well_rest_controller.route('/video', methods=['GET'])
def getWellVideo():
    parser = reqparse.RequestParser()
    parser.add_argument('procedure_id', type=str)
    parser.add_argument('dish_id', type=str)
    parser.add_argument('well_id', type=str)
    code, msg = well_service.getWellVideo(parser.parse_args())
    return make_response(msg, code)

#获取所有大图生成视频的存储路径
@well_rest_controller.route('/video_path', methods=['GET'])
def getWellVideoPath():
    parser = reqparse.RequestParser()
    parser.add_argument('procedure_id', type=str)
    parser.add_argument('dish_id', type=str)
    parser.add_argument('well_id', type=str)
    code, msg = well_service.getWellVideoPath(parser.parse_args())
    return make_response(msg, code)

#查询培养箱
@well_rest_controller.route('/incubator', methods=['GET'])
def queryIncubator():
    code, msg = well_service.queryIncubator()
    return make_response(msg, code)

#查询培养皿
@well_rest_controller.route('/dish', methods=['GET'])
def queryDish():
    parser = reqparse.RequestParser()
    parser.add_argument('incubatorName', type=str)
    code, msg = well_service.queryDish(parser.parse_args())
    return  make_response(msg, code)

#查询采集目录
@well_rest_controller.route('/catalog/list', methods=['GET'])
def queryCollectionCatalog():
    code, msg = well_service.queryCollectionCatalog()
    return make_response(msg, code)

#查询采集目录详情,包括目录下的培养箱,培养皿,用户姓名,开始采集时间,胚胎数量等
@well_rest_controller.route('/catalog/info', methods=['GET'])
def getCollectionCatalogInfo():
    parser = reqparse.RequestParser()
    parser.add_argument('catalogName', type=str)
    return well_service.getCollectionCatalogInfo(parser.parse_args())