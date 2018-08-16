# -*- coding: utf8 -*-
from entity.RestResult import RestResult
import service.front.image_service as image_service
from flask import request, jsonify
from common import uuid,logger
from app import conf
import json,os

def queryClearImageUrl(agrs):
    procedureId = agrs['procedureId']
    dishId = agrs['dishId']
    wellId = agrs['wellId']
    zData = {}
    try:
        #获取JSON文件
        imagePath,path,dishJson = image_service.readDishState(procedureId,dishId)
        clearImageUrlList=[]
        
        if dishJson['finished'] & dishJson['avail'] == 1 : 
            wells = dishJson['wells']
            oneWell = wells[f'{wellId}']
            series = oneWell['series']
            for key in series:
                imageObj={}
                clearImageUrl = path + key + os.path.sep + series[key]['sharp']
                imageObj['clearImageUrl'] = clearImageUrl
                imageObj['timeSeries'] = key
                clearImageUrlList.append(imageObj)
        if not clearImageUrlList:
            return 200, None
        else: 
            return 200, clearImageUrlList
    except:
        return 400, '获取孔的时间序列对应最清晰的URL异常!'


def fenye(datas,pagenum,pagesize):
    if datas and isinstance(pagenum,int) and isinstance(pagesize,int):
        return datas[((pagenum-1)*pagesize):((pagenum-1)*pagesize)+pagesize]