# -*- coding: utf8 -*-
from entity.RestResult import RestResult
import dao.front.patient_mapper as patient_mapper
from flask import request, jsonify
from common import uuid
import json

# 根据输入框的值查询患者姓名
def queryPatientNameList(request):
    # 动态组装查询条件
    sqlCondition = " where 1=1 "  # 动态sql
    filters = {}  # 动态参数
    limit = request.args.get("limit")  # 查询多少条
    query = request.args.get("query")  # 当前输入值
    if query != None and query != "":
        filters["query"] = "%" + query + "%"
        sqlCondition += " and patient_name like :query "

    sqlCondition += " limit " + limit
    result = patient_mapper.queryPatientNameList(sqlCondition, filters)
    patientNameList = list(map(dict, result))
    return jsonify(patientNameList)
