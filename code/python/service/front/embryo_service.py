# -*- coding: utf8 -*-

from entity.RestResult import RestResult
import dao.front.embryo_mapper as embryo_mapper
from flask import request, jsonify
import dao.front.procedure_dish_mapper as procedure_dish_mapper



def queryEmbryoList(id):
    try:
        result = embryo_mapper.queryEmbryoList(id)
        restResult = RestResult(0, "OK", len(result), list(map(dict, result)))
        return 200, jsonify(restResult.__dict__)
    except:
        return 500, '查询胚胎列表异常!'

def signEmbryo(id,embryoFateId):
    try:
        embryo_mapper.signEmbryo(id,embryoFateId)
    except:
        return 500, '标记胚胎结局时发生错误!'
    return 200, '标记胚胎结局成功!'

def getEmbryoById(id):
    try: 
        embryo = embryo_mapper.getEmbryoById(id)
        restResult = RestResult(0, "404", 0, None)
        if embryo is not None:
            restResult = RestResult(0, "OK", 1, dict(embryo))
        return 200, jsonify(restResult.__dict__)
    except:
        return 400, '查询单个胚胎时发生错误!'

def getPatientByEmbryoId(id):
     try: 
         embryo = embryo_mapper.getPatientByEmbryoId(id)
         restResult = RestResult(0, "404", 0, None)
         if embryo is not None:
             restResult = RestResult(0, "OK", 1, dict(embryo))
         return 200, jsonify(restResult.__dict__)
     except:
         return 400, '查询单个胚胎时发生错误!'


def queryEmbryoNumber(agrs):
    try:
        from configparser import ConfigParser
        from task.ini_parser import EmbryoIniParser as parser
        from app import conf
        import json,os

        dishCode = agrs['dishCode']

        dishCodeList = dishCode.split('|')
        for dishCodeStr in dishCodeList:
            catalog = dishCodeStr.split(',')[1]
            if catalog[0] == '.':
                pass  
            else:
                ini_path = conf['EMBRYOAI_IMAGE_ROOT'] + os.path.sep + catalog + os.path.sep + 'DishInfo.ini'
                config = parser(ini_path)
                dishes = [f'Dish{i}Info' for i in range(1, 10) if f'Dish{i}Info' in config]
                wells = [f'Well{i}Avail' for i in range(1, 13)]
                embryo_number = len([index for d in dishes for index,w in enumerate(wells) if config[d][w]=='1'])

        return 200, jsonify(embryo_number)
    except:
        return 500, '查询胚胎数量异常!'


def findEmbroyoInfo(args) :
    imagePath = args["imagePath"]
    dishId = args["dishId"]
    wellCode = args["wellCode"]

    procedureId,embryoId = procedure_dish_mapper.queryEmbryoId(imagePath,dishId,wellCode)

    return procedureId,dishId,embryoId 

