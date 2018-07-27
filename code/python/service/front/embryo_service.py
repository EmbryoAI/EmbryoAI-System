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