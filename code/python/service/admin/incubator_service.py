# -*- coding: utf8 -*-

from entity.Incubator import Incubator
from entity.RestResult import RestResult
import dao.admin.incubator_mapper as incubator_mapper
from flask import request, jsonify
from common import uuid
import time
import hashlib
import json
import random;

def updateIncubator (username, password):
    try:
        params = {'username': username, 'password': password}
        incubator_mapper.updateIncubator(params)
    except:
        return 400, {'msg': '修改培养箱密码时发生错误'}
    return 202, {'msg': '修改成功'}

def insertIncubator(request):

    id = uuid()
    incubatorBrand = request.form.get('incubatorBrand')
    if incubatorBrand == "":
        return 400, '培养箱品牌不能为空!'
    incubatorType = request.form.get('incubatorType')
    if incubatorType == "":
        return 400, '培养箱型号不能为空!'
    incubatorDescription = request.form.get('incubatorDescription')
    if incubatorDescription == "":
        return 400, '培养箱描述不能为空!'

    nowTime=time.strftime("%Y%m%d%H%M%S");#生成当前时间  
    randomNum=random.randint(0,100);#生成的随机整数n，其中0<=n<=100  
    if randomNum<=10:  
        randomNum=str(0)+str(randomNum);  
    incubatorCode=str(nowTime)+str(randomNum);

    create_time = update_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 
    delFlag = 0;
    incubator = Incubator(id=id, incubatorCode=incubatorCode,incubatorBrand=incubatorBrand,incubatorType=incubatorType,incubatorDescription=incubatorDescription,delFlag=delFlag,createTime=create_time, 
        updateTime=update_time)
    try:
        incubator_mapper.insertIncubator(incubator)
    except:
        return 400, '新增培养箱异常!'
    return 200, incubator.to_dict()

def updateIncubator(request):
    id = request.form.get('id')
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
    delFlag = 0;
    params = {'id': id, 'incubatorBrand': incubatorBrand, 'incubatorType': incubatorType, 'incubatorDescription': incubatorDescription, 'updateTime': updateTime}
    try:
        incubator_mapper.updateIncubator(params)
    except:
        return 400, '新增培养箱异常!'
    return 200, ""


def findIncubatorById(id):
    return incubator_mapper.findIncubatorById(id)

def queryIncubatorList(request):
    try:
        page = request.args.get('page');
        if page==None:
           page=1
        limit = request.args.get('limit');
        if limit==None:
            limit=10
        
        #动态组装查询条件
        incubatorCode = request.args.get('incubatorCode');
        filters = {};
        if incubatorCode!=None:
            filters['incubatorCode']=incubatorCode
            
        #查詢列表
        pagination = incubator_mapper.queryIncubatorList(int(page),int(limit),filters);
        incubatorList = pagination.items
        incubatorList = list(map(lambda x: x.to_dict(),incubatorList))
        
        #查询总数
        count = pagination.total;
        
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