# -*- coding: utf8 -*-

from entity.Procedure import Procedure
from entity.RestResult import RestResult
import dao.front.statistics_mapper as statistics_mapper
import dao.front.patient_mapper as patient_mapper
from flask import request, jsonify
from common import uuid
import re

def embryoOutcome(request):
    try: 
        #动态组装查询条件
        sqlCondition = ""#动态sql
        filters = {}#动态参数
        
        ecTime = request.args.get('ecTime')#取卵日期
        if ecTime!=None and ecTime!="":
            ecTimeList = re.split('~', ecTime)
            filters['ecTimeStart']=ecTimeList[0].strip()+" 00:00:00" #首尾去空格
            filters['ecTimeEnd']=ecTimeList[1].strip()+" 23:59:59" #首尾去空格
            sqlCondition += " and  c.cap_end_time >= :ecTimeStart "
            sqlCondition += " and  c.cap_end_time <= :ecTimeEnd "
 
        #查詢列表
        result = statistics_mapper.embryoOutcome(sqlCondition,filters)
        embryoOutcomeList = list(map(dict, result))
        
    except:
        return 400, '查询胚胎结局统计时发生错误!'
    restResult = RestResult(0, "OK",len(embryoOutcomeList), embryoOutcomeList)
    return jsonify(restResult.__dict__)

def milestoneEmbryos():
    try: 
        #查詢列表
        result = statistics_mapper.milestoneEmbryos()
        milestoneEmbryosList = list(map(dict, result))
    except:
        return 400, '查询周期中里程碑点胚胎数时发生错误!'
    restResult = RestResult(0, "OK",len(milestoneEmbryosList), milestoneEmbryosList)
    return jsonify(restResult.__dict__)

def pregnancyRate(request):
    try: 
        #动态组装查询条件
        sqlCondition = " where 1=1 "#动态sql
        filters = {}#动态参数
        
        ecTime = request.args.get('ecTime')#取卵日期
        if ecTime!=None and ecTime!="":
            ecTimeList = re.split('~', ecTime)
            filters['ecTimeStart']=ecTimeList[0].strip()+" 00:00:00" #首尾去空格
            filters['ecTimeEnd']=ecTimeList[1].strip()+" 23:59:59" #首尾去空格
            sqlCondition += " and  a.cap_end_time >= :ecTimeStart "
            sqlCondition += " and  a.cap_end_time <= :ecTimeEnd "
        #查詢列表
        result = statistics_mapper.pregnancyRate(sqlCondition,filters)
        pregnancyRateList = list(map(dict, result))
    except:
        return 400, '查询妊娠率统计时发生错误!'
    restResult = RestResult(0, "OK",len(pregnancyRateList), pregnancyRateList)
    return jsonify(restResult.__dict__)
