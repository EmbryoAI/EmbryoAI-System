# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
import logUtils
from app import db
import service.front.patient_service as patient_service
from entity.User import User
import time

patient_rest_controller = Blueprint('patient_rest_controller', __name__)
url_prefix = '/api/v1/patient'

#根据输入框的值查询患者姓名
@patient_rest_controller.route('/name/list', methods=['GET'])
def queryPatientNameList():
    logUtils.info('patient_rest_controller.queryPatientNameList-根据输入框的值查询患者姓名')
    return patient_service.queryPatientNameList(request)