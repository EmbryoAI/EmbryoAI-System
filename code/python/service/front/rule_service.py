# -*- coding: utf8 -*-

from entity.Rule import Rule
import dao.front.rule_dao as rule_dao
from flask import request, jsonify
from common import parse_date
from common import uuid
import re
import time
import datetime
from app import current_user

def save(request):
    id = uuid()
    milestone = Milestone(id=id, embryoId=embryoId,milestoneId=milestoneId,milestoneTime=milestoneTime,milestoneElapse=milestoneElapse,
                          userId=userId,milestoneType=milestoneType,milestonePath=milestonePath)
    return 200, milestone.to_dict()

def queryRuleList():
    userId = current_user.id
    result = rule_dao.queryRuleListByUserId(userId)
    ruleList = list(map(lambda x: x.to_dict(),result))
    return ruleList
"""
    获取字典的里程碑节点，以及对应的规则ID
"""
def getRuleById(ruleId):
    try:
        userId = current_user.id
        result = rule_dao.getRuleById(ruleId,userId)
        rule = result.to_dict()
        return 200,rule
    except:
        return 400,"根据ID获取规则失败"
    