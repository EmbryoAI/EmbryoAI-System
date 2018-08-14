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
