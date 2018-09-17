from flask import Blueprint, jsonify,render_template,request
from common import logger
from app import login_required
from flask_restful import reqparse
import service.front.rule_service as rule_service
import dao.front.dict_dao as dict_dao
import json

'''评分规则配置页面 '''

rule_controller = Blueprint('rule_controller', __name__)
url_prefix = '/front/rule'

@rule_controller.route('/', methods=['GET'])
@login_required
def main():
    logger().info('rule_controller.rule评分规则配置页面 ')
    #当前用户的评分标准
    ruleList = rule_service.queryRuleList()
    #获取里程碑字典值字符串，由于需要排序需使用json.dumps(msg, ensure_ascii=False)
    result = dict_dao.queryDictListByClass("milestone")
    dictList = list(map(lambda x: x.to_dict(),result))
    dictStr = json.dumps(dictList, ensure_ascii=False)
    
    return render_template('front/rule/rule.html',ruleList=ruleList,dictStr=dictStr,dictList=dictList)

"""
    跳转到新增标准 页面
"""
@rule_controller.route('/toRuleSave', methods=['GET'])
@login_required
def toRuleSave():
    ruleId = request.args.get('ruleId')
    print(ruleId)
    rule = None
    if ruleId!=None:
        code,rule = rule_service.getRuleById(ruleId)
    return render_template('front/rule/rule_save.html',rule=rule)


"""
    跳转到新增规则JSON页面
"""
@rule_controller.route('/toRuleJsonSave/<string:ruleId>/<string:jsonKey>/<string:index>', methods=['GET'])
@login_required
def toRuleJsonSave(ruleId,jsonKey,index):
    #获取条件
    result = dict_dao.queryDictListByClass("criteria_type")
    conditionList = list(map(lambda x: x.to_dict(),result))
    
    #获取符号
    result = dict_dao.queryDictListByClass("criteria_op")
    symbolList = list(map(lambda x: x.to_dict(),result))
    
    #获取指定的规则 JSON
    ruleJson = rule_service.getRuleJson(ruleId,jsonKey,index)
    return render_template('front/rule/rule_json_save.html',ruleId=ruleId
                           ,conditionList=conditionList,symbolList=symbolList
                           ,jsonKey=jsonKey,index=index,ruleJson=ruleJson)