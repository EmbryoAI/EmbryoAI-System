# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
from common import logger
from app import db, login_required
import service.front.dict_service as dict_service
import time

dish_rest_controller = Blueprint('dish_rest_controller', __name__)
url_prefix = '/api/v1/dish'

#根据procedureId,皿ID查询皿下面的时间序列
@dish_rest_controller.route('/list/<string:id>/<string:code>', methods=['GET'])
@login_required
def querySeriesList(id, code):
    print(id)
    print(code)
    return 'OK'
