# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort
from flask_restful import reqparse
import logUtils
import service.front.rule_service as rule_service
from app import login_required 

rule_rest_controller = Blueprint('rule_rest_controller', __name__)
url_prefix = '/api/v1/rule'

'''  
    新增和修改标准
'''
@rule_rest_controller.route('/save', methods=['POST'])
@login_required
def save():
    logUtils.info('rule_rest_controller.save-新增和修改标准')
    code, rule = rule_service.save(request)
    return make_response(jsonify(rule), code)

'''
    新增和修改规则JSON
'''
@rule_rest_controller.route('/saveRuleJson', methods=['POST'])
@login_required
def saveRuleJson():
    logUtils.info('rule_rest_controller.saveRuleJson-新增和修改规则JSON')
    code, rule = rule_service.saveRuleJson(request)
    return make_response(jsonify(rule), code)

'''
    刪除规则JSON
'''
@rule_rest_controller.route('/delete/<string:ruleId>/<string:jsonKey>/<string:index>', methods=['GET'])
@login_required
def deleteRuleJson(ruleId,jsonKey,index):
    logUtils.info('rule_rest_controller.deleteRuleJson-刪除规则JSON')
    code, rule = rule_service.deleteRuleJson(ruleId,jsonKey,index)
    return make_response(jsonify(rule), code)

''' 根据规则ID查询出对应的规则列表
    @param ruleId: 规则id
'''
@rule_rest_controller.route('/get/<string:ruleId>', methods=['GET'])
@login_required
def getRuleById(ruleId):
    logUtils.info('rule_rest_controller.getRuleById-根据规则ID查询出对应的规则列表')
    code, rule = rule_service.getRuleById(ruleId)
    return make_response(jsonify(rule), code)

''' 设置当前规则为默认
    @param ruleId: 规则id
'''
@rule_rest_controller.route('/setDefault/<string:ruleId>', methods=['GET'])
@login_required
def setDefault(ruleId):
    logUtils.info('rule_rest_controller.setDefault-设置当前规则为默认')
    code, rule = rule_service.setDefault(ruleId)
    return make_response(jsonify(rule), code)

#查询所有评分规则
@rule_rest_controller.route('/list', methods=['GET'])
@login_required
def findAllRules():
    logUtils.info('rule_rest_controller.findAllRules-查询所有评分规则')
    return rule_service.findAllRules()