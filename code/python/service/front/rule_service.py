# -*- coding: utf8 -*-

from entity.Rule import Rule
import dao.front.rule_dao as rule_dao
import dao.front.dict_dao as dict_dao
from flask import request, jsonify
from common import parse_date
from common import uuid
import re
import time
import datetime
from app import current_user
import json

"""
    新增和修改标准
"""
def save(request):
    try:
        id = uuid()
        #标准名称
        ruleName = request.form.get('ruleName')
        if not ruleName:
           return 400, '标准名称不能为空!'
        #描述
        description = request.form.get('description')
        if not description:
           return 400, '描述不能为空!'
     
        ruleId = request.form.get('ruleId')
        userId = current_user.id
        if not ruleId: #为新增
           id = uuid()
           createTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
           #如果为新增则 根据里程碑节点生成规则json串
           #查询字典表里程碑的节点
           result = dict_dao.queryDictListByClass("milestone")
           dictList = list(map(lambda x: x.to_dict(),result))
           tableObj={}
           procedureViewList=[]
           for key in dictList:
               tableObj[key['dictValue']] = procedureViewList
           dataJson = json.dumps(tableObj, ensure_ascii=False)
           updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
          
           isDefault = 0
           delFlag = 0
           rule = Rule(id=id, userId=userId,ruleName=ruleName,description=description,createTime=createTime,
                              updateTime=updateTime,delFlag=delFlag,isDefault=isDefault,dataJson=dataJson)
           rule_dao.insertRule(rule)
        else:#修改标准
           rule = rule_dao.getRuleById(ruleId,userId)
           updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
           rule.updateTime = updateTime
           rule.ruleName = ruleName
           rule.description = description
           rule_dao.updateRule(rule)
        return 200, "保存成功!"
    except Exception as e:
        return 400, "系统异常，保存失败!"

"""
    新增和修改规则JSON
"""
def saveRuleJson(request):
    try:
        #条件
        condition = request.form.get('condition')
        if not condition:
           return 400, '条件不能为空!'
        #符号
        symbol = request.form.get('symbol')
        if not symbol:
           return 400, '符号不能为空!'
        #判断值
        value = request.form.get('value')
        if not value:
           return 400, '判断值不能为空!'
        #分值
        score = request.form.get('score')
        if not score:
           return 400, '分值不能为空!'
        #权重
        weight = request.form.get('weight')
        if not weight:
           return 400, '权重不能为空!'
        
     
        ruleId = request.form.get('ruleId')
        jsonKey = request.form.get('jsonKey')
        index = request.form.get('index')
        userId = current_user.id
        jsonObj={}
        rule = rule_dao.getRuleById(ruleId,userId)
        data = json.loads(rule.dataJson)#把JSON字符串转为对象
        objList = data[jsonKey]
        if index==None or index=="null":#如果为空则为新增
            index = uuid()
            jsonObj["index"] = index
            jsonObj["condition"] = condition
            jsonObj["symbol"] = symbol
            jsonObj["value"] = value
            jsonObj["score"] = score
            jsonObj["weight"] = weight
            objList.append(jsonObj)
        else:#如果不为空，则为修改
            for obj in objList:
                if obj["index"]==index:
                   obj["index"] = index
                   obj["condition"] = condition
                   obj["symbol"] = symbol
                   obj["value"] = value
                   obj["score"] = score
                   obj["weight"] = weight
        data[jsonKey] = objList;
        dataJson = json.dumps(data, ensure_ascii=False)
        
        updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        rule.updateTime = updateTime
        rule.dataJson = dataJson
        rule_dao.updateRule(rule)
        return 200, "保存成功!"
    except Exception as e:
        return 400, "系统异常，保存失败!"

def deleteRuleJson(ruleId,jsonKey,index):
    try:
        userId = current_user.id
        jsonObj={}
        rule = rule_dao.getRuleById(ruleId,userId)
        data = json.loads(rule.dataJson)#把JSON字符串转为对象
        objList = data[jsonKey]
        for obj in objList:
            if obj["index"]==index:
                objList.remove(obj)
        data[jsonKey] = objList;
        dataJson = json.dumps(data, ensure_ascii=False)
        print(dataJson)
        updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        rule.updateTime = updateTime
        rule.dataJson = dataJson
        rule_dao.updateRule(rule)
        return 200, "刪除成功!"
    except Exception as e:
        return 400, "系统异常，刪除失败!"

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
    
"""
    根据规则ID和jsonKey和index获取指定规则JSON
"""
def getRuleJson(ruleId,jsonKey,index):
        userId = current_user.id
        rule = rule_dao.getRuleById(ruleId,userId)
        data = json.loads(rule.dataJson)#把JSON字符串转为对象
        objList = data[jsonKey]
        for obj in objList:
            if obj["index"]==index:
               return obj