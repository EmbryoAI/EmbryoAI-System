# -*- coding: utf8 -*-

from entity.Procedure import Procedure
from entity.RestResult import RestResult
import dao.front.procedure_mapper as procedure_mapper
from flask import request, jsonify
from common import uuid
import time
import hashlib
import json
import random;

def queryProcedureList(request):
    try:
        page = request.args.get('page');
        if page==None:
           page=1
        limit = request.args.get('limit');
        if limit==None:
            limit=10
        
        #动态组装查询条件
     
        sqlCondition = " where 1=1 ";#动态sql
        filters = {};#动态参数
        userName = request.args.get('userName');#用户名字
        if userName!=None and userName!="":
            filters['userName']=userName
            sqlCondition = " and pa.patient_name=%s "
        
        medicalRecordNo = request.args.get('medicalRecordNo');#病历号
        if medicalRecordNo!=None and medicalRecordNo!="":
            filters['medicalRecordNo']=medicalRecordNo
            sqlCondition = " and pr.medical_record_no=%s "
        
            
        #查詢列表
        result = procedure_mapper.queryProcedureList(int(page),int(limit),filters);
        procedureList = list(map(dict, result))
        #查询总数
        count = procedure_mapper.queryProcedureCount(filters);
        
    except:
        return 400, '查询培养箱列表时发生错误!'
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
