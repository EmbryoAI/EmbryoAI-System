# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
from common import logger
from app import db
import service.front.feedback_service as feedback_service
from entity.User import User
import time


feedback_rest_controller = Blueprint('feedback_rest_controller', __name__)
url_prefix = '/api/v1/feedback'

#保存病历回访数据
@feedback_rest_controller.route('/', methods=['POST'])
def save():
    code, msg = feedback_service.save_feedback(request)
    return make_response(jsonify(msg), code)

#查询病历回访数据
@feedback_rest_controller.route('/<string:id>', methods=['GET'])
def geiFeedbackInfo(id):
    return feedback_service.getFeedbackInfo(id)