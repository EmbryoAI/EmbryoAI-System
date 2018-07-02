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
        incubatorCode = request.args.get('incubatorCode');
        filters = {};
        if incubatorCode!=None and incubatorCode!="":
            filters['incubatorCode']=incubatorCode
            
        #查詢列表
        result = procedure_mapper.queryProcedureList(int(page),int(limit),filters);
        
        procedureList = list(map(dict, result))
#         procedureList = list(map(lambda x: x.to_dict(),result))
        
        #查询总数
        count = procedure_mapper.queryProcedureCount(filters);
        
    except:
        return 400, '查询培养箱列表时发生错误!'
    restResult = RestResult(0, "OK", count, procedureList)
    return jsonify(restResult.__dict__)

def getProcedureDetail(id):
    try:
        result = procedure_mapper.getProcedureById(id)
        restResult = RestResult(0, "OK", 1, list(map(dict, result)))
        return jsonify(restResult.__dict__)
    except:
        return 400, '查询病历详情时发生错误!'
