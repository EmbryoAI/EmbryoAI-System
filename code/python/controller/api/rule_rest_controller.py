# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort
from flask_restful import reqparse
from common import logger
import service.front.rule_service as rule_service
from app import login_required 

rule_rest_controller = Blueprint('rule_rest_controller', __name__)
url_prefix = '/api/v1/rule'

'''  
    新增和修改规则
'''
@rule_rest_controller.route('/save', methods=['POST'])
@login_required
def save():
    code, rule = rule_service.save(request)
    return make_response(jsonify(rule), code)

''' 根据规则ID查询出对应的规则列表
    @param ruleId: 规则id
'''
@rule_rest_controller.route('/get/<string:ruleId>', methods=['GET'])
@login_required
def getRuleById(ruleId):
    code, rule = rule_service.getRuleById(ruleId)
    return make_response(jsonify(rule), code)