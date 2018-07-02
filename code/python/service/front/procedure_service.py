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
        pagination = procedure_mapper.queryProcedureList(int(page),int(limit),filters);
        paginationList = pagination.items
        paginationList = list(map(lambda x: x.to_dict(),paginationList))
        
        #查询总数
        count = pagination.total;
        
    except:
        return 400, '查询培养箱列表时发生错误!'
    restResult = RestResult(0, "OK", count, paginationList)
    return jsonify(restResult.__dict__)

def getProcedureDetail(id):
    try:
        result = procedure_mapper.getProcedureById(id)
        restResult = RestResult(0, "OK", 1, list(map(dict, result)))
        return jsonify(restResult.__dict__)
    except:
        return 400, '查询病历详情时发生错误!'
