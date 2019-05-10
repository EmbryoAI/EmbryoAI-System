# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
import logUtils
from app import db, login_required
import service.front.dish_service as dish_service
import time
import json

dish_rest_controller = Blueprint('dish_rest_controller', __name__)
url_prefix = '/api/v1/dish'

#根据procedureId,皿ID查询皿下面的时间序列
@dish_rest_controller.route('/list', methods=['GET'])
@login_required
def querySeriesList():
    logUtils.info('dish_controller.querySeriesList-皿ID查询皿下面的时间序列')
    parser = reqparse.RequestParser()
    parser.add_argument('procedure_id', type=str)
    parser.add_argument('dish_id', type=str)
    parser.add_argument('well_id', type=str)
    parser.add_argument('seris', type=str)
    parser.add_argument('cell_id', type=str)
    code, msg = dish_service.querySeriesList(parser.parse_args())
    return make_response(msg, code)

#左右滚动
@dish_rest_controller.route('/scroll', methods=['GET'])
@login_required
def queryScrollbarSeriesList():
    logUtils.info('dish_controller.queryScrollbarSeriesList-左右滚动')
    parser = reqparse.RequestParser()
    parser.add_argument('procedure_id', type=str)
    parser.add_argument('dish_id', type=str)
    parser.add_argument('well_id', type=str)
    parser.add_argument('current_seris', type=str)
    parser.add_argument('direction', type=str)
    code, msg = dish_service.queryScrollbarSeriesList(parser.parse_args())
    return make_response(msg, code)

''' 根据培养箱id查询培养箱里所有皿的信息 '''
@dish_rest_controller.route('/loadDishList',methods=['GET'])
@login_required
def loadDishList():
    logUtils.info('dish_controller.loadDishList-根据培养箱id查询培养箱里所有皿的信息')
    parser = reqparse.RequestParser()
    parser.add_argument('incubatorId', type=str)
    parser.add_argument('procedureId', type=str)
    return dish_service.loadDishByIncubatorId(parser.parse_args())


#根据procedureId,皿ID查询某个孔的时间序列，不包含缩略图路径
@dish_rest_controller.route('/loadSeriesList', methods=['GET'])
@login_required
def loadSeriesList():
    logUtils.info('dish_controller.loadSeriesList-皿ID查询某个孔的时间序列')
    parser = reqparse.RequestParser()
    parser.add_argument('procedureId', type=str)
    parser.add_argument('dishId', type=str)
    parser.add_argument('wellId', type=str)
    
    code,result = dish_service.getSeriesList(parser.parse_args())
    return make_response(result, code)


"""根据皿ID获取胚胎评分表"""
@dish_rest_controller.route('/emGrade/<string:dishId>', methods=['GET'])
@login_required
def emGrade(dishId):
    logUtils.info('dish_controller.emGrade-胚胎评分表')
    code, emGradeList = dish_service.emGrade(dishId)
    return make_response(jsonify(emGradeList), code)

"""根据皿ID获取胚胎总览表"""
@dish_rest_controller.route('/emAll/<string:dishId>', methods=['GET'])
@login_required
def emAll(dishId):
    logUtils.info('dish_controller.emAll-胚胎总览表')
    code, emAllList = dish_service.emAll(dishId)
    return make_response(json.dumps(emAllList, ensure_ascii=False), code)