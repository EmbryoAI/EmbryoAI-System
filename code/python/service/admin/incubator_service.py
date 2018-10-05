# -*- coding: utf8 -*-

from entity.Incubator import Incubator
from entity.RestResult import RestResult
import dao.admin.incubator_mapper as incubator_mapper
from flask import request, jsonify
from common import uuid
import time
import hashlib
import json
import random

def updateIncubator (username, password):
    try:
        params = {'username': username, 'password': password}
        incubator_mapper.updateIncubator(params)
    except:
        return 400, {'msg': '修改培养箱时发生错误'}
    return 202, {'msg': '修改成功'}

def insertIncubator(request):

    id = uuid()
    
    incubatorCode = request.form.get('incubatorCode')
    if incubatorCode == "":
       return 400, '培养箱编码不能为空!'
    incubatorBrand = request.form.get('incubatorBrand')
    if incubatorBrand == "":
        return 400, '培养箱品牌不能为空!'
    incubatorType = request.form.get('incubatorType')
    if incubatorType == "":
        return 400, '培养箱型号不能为空!'
    incubatorDescription = request.form.get('incubatorDescription')
    if incubatorDescription == "":
        return 400, '培养箱描述不能为空!'
    
    create_time = update_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 
    delFlag = 0
    incubator = Incubator(id=id, incubatorCode=incubatorCode,incubatorBrand=incubatorBrand,incubatorType=incubatorType,incubatorDescription=incubatorDescription,delFlag=delFlag,createTime=create_time, 
        updateTime=update_time)
    try:
        incubatorOld = incubator_mapper.findIncubatorByCode(incubatorCode)
        if incubatorOld!=None:
            return 400, '当前培养箱编码已存在，请您使用其他编码!'
        
        incubator_mapper.insertIncubator(incubator)
    except:
        return 400, '新增培养箱异常!'
    return 200, "新增培养箱成功!"

def updateIncubator(request):
    id = request.form.get('id')
    incubatorCode = request.form.get('incubatorCode')
    if incubatorCode == "":
       return 400, '培养箱编码不能为空!'
    incubatorBrand = request.form.get('incubatorBrand')
    if incubatorBrand == "":
        return 400, '培养箱品牌不能为空!'
    incubatorType = request.form.get('incubatorType')
    if incubatorType == "":
        return 400, '培养箱型号不能为空!'
    incubatorDescription = request.form.get('incubatorDescription')
    if incubatorDescription == "":
        return 400, '培养箱描述不能为空!'
    updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 
    delFlag = 0
    params = {'id': id, 'incubatorCode': incubatorCode,'incubatorBrand': incubatorBrand, 'incubatorType': incubatorType, 'incubatorDescription': incubatorDescription, 'updateTime': updateTime}
    try:
        incubatorOld = incubator_mapper.findIncubatorByCode(incubatorCode)
        if incubatorOld!=None:
             incubatorbenshen = incubator_mapper.findIncubatorById(id)
             if incubatorOld.incubatorCode!=incubatorbenshen.incubatorCode:
                  return 400, '当前培养箱编码已存在，请您使用其他编码!'
              
        incubator_mapper.updateIncubator(params)
    except:
        return 400, '编辑培养箱异常!'
    return 200, "编辑培养箱成功"


def findIncubatorById(id):
    return incubator_mapper.findIncubatorById(id)

def queryIncubatorList(request):
    try:
        page = request.args.get('page')
        if page==None:
           page=1
        limit = request.args.get('limit')
        if limit==None:
            limit=10
        
        #动态组装查询条件
        incubatorCode = request.args.get('incubatorCode')
        filters = {}
        if incubatorCode!=None and incubatorCode!="":
            filters['incubatorCode']=incubatorCode
            
        #查詢列表
        pagination = incubator_mapper.queryIncubatorList(int(page),int(limit),filters)
        incubatorList = pagination.items
        incubatorList = list(map(lambda x: x.to_dict(),incubatorList))
        
        #查询总数
        count = pagination.total
        
    except:
        return 400, '查询培养箱列表时发生错误!'
    restResult = RestResult(0, "OK", count, incubatorList)
    return jsonify(restResult.__dict__)

def deleteIncubator(id):
    try:
        params = {'id': id, 'delFlag': 1}
        incubator_mapper.deleteIncubator(params)
    except:
        return 400, {'msg': '删除培养箱时发生错误'}
    return 204, None