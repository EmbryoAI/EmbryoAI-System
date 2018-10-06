# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
from common import logger
from app import db, login_required
import service.front.dish_service as dish_service
import time

dish_rest_controller = Blueprint('dish_rest_controller', __name__)
url_prefix = '/api/v1/dish'

#根据procedureId,皿ID查询皿下面的时间序列
@dish_rest_controller.route('/list', methods=['GET'])
@login_required
def querySeriesList():
    parser = reqparse.RequestParser()
    parser.add_argument('procedure_id', type=str)
    parser.add_argument('dish_id', type=str)
    parser.add_argument('well_id', type=str)
    parser.add_argument('seris', type=str)
    parser.add_argument('cell_id', type=str)
    return dish_service.querySeriesList(parser.parse_args())

#左右滚动
@dish_rest_controller.route('/scroll', methods=['GET'])
@login_required
def queryScrollbarSeriesList():
    parser = reqparse.RequestParser()
    parser.add_argument('procedure_id', type=str)
    parser.add_argument('dish_id', type=str)
    parser.add_argument('well_id', type=str)
    parser.add_argument('current_seris', type=str)
    parser.add_argument('direction', type=str)
    return dish_service.queryScrollbarSeriesList(parser.parse_args())

''' 根据培养箱id查询培养箱里所有皿的信息 '''
@dish_rest_controller.route('/loadDishList',methods=['GET'])
@login_required
def loadDishList():
    parser = reqparse.RequestParser()
    parser.add_argument('incubatorId', type=str)
    parser.add_argument('procedureId', type=str)
    return dish_service.loadDishByIncubatorId(parser.parse_args())


#根据procedureId,皿ID查询某个孔的时间序列，不包含缩略图路径
@dish_rest_controller.route('/loadSeriesList', methods=['GET'])
@login_required
def loadSeriesList():
    parser = reqparse.RequestParser()
    parser.add_argument('procedureId', type=str)
    parser.add_argument('dishId', type=str)
    parser.add_argument('wellId', type=str)
    return dish_service.getSeriesList(parser.parse_args())


"""根据皿ID获取胚胎评分表"""
@dish_rest_controller.route('/emGrade/<string:dishId>', methods=['GET'])
@login_required
def emGrade(dishId):
    logger().info('dish_controller.胚胎评分表')
    code, emGradeList = dish_service.emGrade(dishId)
    return make_response(jsonify(emGradeList), code)

"""根据皿ID获取胚胎总览表"""
@dish_rest_controller.route('/emAll/<string:dishId>', methods=['GET'])
@login_required
def emAll(dishId):
    logger().info('dish_controller.胚胎总览表')
    code, emAllList = dish_service.emAll(dishId)
    return make_response(jsonify(emAllList), code)