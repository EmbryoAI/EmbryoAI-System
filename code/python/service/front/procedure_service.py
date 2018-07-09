# -*- coding: utf8 -*-

from entity.Procedure import Procedure
from entity.RestResult import RestResult
import dao.front.procedure_mapper as procedure_mapper
import dao.front.patient_mapper as patient_mapper
from flask import request, jsonify
from common import uuid
import re

def queryProcedureList(request):
    try:
        page = request.args.get('page')
        if page==None:
           page=1
        limit = request.args.get('limit')
        if limit==None:
            limit=10

        #动态组装查询条件
        sqlCondition = " where 1=1 "#动态sql
        filters = {}#动态参数
        userName = request.args.get('userName')#用户名字
        if userName!=None and userName!="":
            filters['userName']="%"+userName+"%"
            sqlCondition += " and pa.patient_name like :userName "

        medicalRecordNo = request.args.get('medicalRecordNo')#病历号
        if medicalRecordNo!=None and medicalRecordNo!="":
            filters['medicalRecordNo']="%"+medicalRecordNo+"%"
            sqlCondition += " and pr.medical_record_no like :medicalRecordNo "

        state = request.args.get('state')#状态
        if state!=None and state!="":
            filters['state']=state
            sqlCondition += " and  d2.dict_value=:state "
            
        ecTime = request.args.get('ecTime')#取卵日期
        if ecTime!=None and ecTime!="":
            ecTimeList = re.split('~', ecTime)
            filters['ecTimeStart']=ecTimeList[0].strip()+" 00:00:00" #首尾去空格
            filters['ecTimeEnd']=ecTimeList[1].strip()+" 23:59:59" #首尾去空格
            sqlCondition += " and  pr.ec_time >= :ecTimeStart "
            sqlCondition += " and  pr.ec_time <= :ecTimeEnd "
        
        insemiTime = request.args.get('insemiTime')#受精日期
        if insemiTime!=None and insemiTime!="":
            insemiTimeList = re.split('~', insemiTime)
            filters['insemiTimeStart']=insemiTimeList[0].strip()+" 00:00:00" #首尾去空格
            filters['insemiTimeEnd']=insemiTimeList[1].strip()+" 23:59:59" #首尾去空格
            sqlCondition += " and  pr.insemi_time >= :insemiTimeStart "
            sqlCondition += " and  pr.insemi_time <= :insemiTimeEnd "
 
        #查詢列表
        result = procedure_mapper.queryProcedureList(int(page),int(limit),sqlCondition,filters)
        procedureList = list(map(dict, result))
        #查询总数
        count = procedure_mapper.queryProcedureCount(sqlCondition,filters)
        
    except:
        return 400, '查询病历列表时发生错误!'
    restResult = RestResult(0, "OK", count, procedureList)
    return jsonify(restResult.__dict__)

def getProcedureDetail(id):
    try: 
        result = procedure_mapper.getProcedureById(id)
        restResult = RestResult(0, "404", 0, None)
        if result is not None:
            restResult = RestResult(0, "OK", 1, dict(result))
        return jsonify(restResult.__dict__)
    except:
        return 400, '查询病历详情时发生错误!'

def updateProcedure(request):
    id = request.form.get('id')
    mobile = request.form.get('mobile')
    email = request.form.get('email')
    memo = request.form.get('memo')
    try:
        procedure_mapper.update(id, memo)
        patient_mapper.update(id, mobile, email)
    except:
        return 500, '修改病历详情时发生错误!'
    return 200, '修改病历详情成功!'

def queryMedicalRecordNoList(request):
        #动态组装查询条件
       sqlCondition = " where 1=1 " #动态sql
       filters = {}#动态参数
       limit = request.args.get('limit')#查询多少条
       query = request.args.get('query')#当前输入值
       if query!=None and query!="":
           filters['query']="%"+query+"%"
           sqlCondition += " and medical_record_no like :query "
           
       sqlCondition += " limit "+limit
       result = procedure_mapper.queryMedicalRecordNoList(sqlCondition,filters)
       procedureList = list(map(dict, result))
       return jsonify(procedureList)