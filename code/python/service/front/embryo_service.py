# -*- coding: utf8 -*-

from entity.RestResult import RestResult
import dao.front.embryo_mapper as embryo_mapper
from flask import request, jsonify



def queryEmbryoList(id):
    result = embryo_mapper.queryEmbryoList(id)
    restResult = RestResult(0, "OK", len(result), list(map(dict, result)))
    return jsonify(restResult.__dict__)

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
        return jsonify(restResult.__dict__)
    except:
        return 400, '查询单个胚胎时发生错误!'

def quertEmbryoNumber(agrs):
    dishCode = agrs['dishCode']
    print(dishCode)
    from configparser import ConfigParser
    from app import conf
    import json,os
    config = ConfigParser()

    list=[]
    dishCodeList = dishCode.split('|')
    for dishCodeStr in dishCodeList:
        catalog = dishCodeStr.split(',')[1]
        config.readfp(open(conf['EMBRYOAI_IMAGE_ROOT'] + catalog + os.path.sep + 'DishInfo.ini'))
        catalog_path = conf['EMBRYOAI_IMAGE_ROOT'] + catalog
        dirs = os.listdir(catalog_path)

        for dir in dirs:
            dish_path = catalog_path + os.path.sep + dir
            if os.path.isdir(dish_path):  
                if dir[0] == '.':  
                    pass  
                else:
                    print(dir)
                    for i in range(1, 12, 1):

                        dir = dir.lower()
                        dir = dir[1:len(dir)]
                        dir = f'D{dir}'
                        print(dir)

                        well = f'Well{i}Avail'
                        result = config.get(f'{dir}Info',well)
                        print(result)
                        if result == '1':
                            list.append(i)
    return jsonify(list)