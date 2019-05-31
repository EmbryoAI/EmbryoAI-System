# -*- coding: utf8 -*-

from flask import jsonify
from entity.RestResult import RestResult
import dao.front.dict_dao as dict_dao
import logUtils as logger

def queryDictListByClass(dictClass):
    try:
        #查詢列表
        result = dict_dao.queryDictListByClass(dictClass)
        dictList = list(map(lambda x: x.to_dict(),result))
    except:
        return 400, '根据字典类别获取对应的字典列表发生错误!'
    restResult = RestResult(0, "OK", len(dictList), dictList)
    return jsonify(restResult.__dict__)


def queryDictListByClassS(dictClass):
    try:
        #查詢列表
        result = dict_dao.queryDictListByClassS(dictClass)
        dictList = list(map(lambda x: x.to_dict(),result))
    except:
        return 400, '根据逗号隔开多个字典类别获取列表发生错误!'
    restResult = RestResult(0, "OK", len(dictList), dictList)
    return jsonify(restResult.__dict__)

def queryDictListByDictParentId(dictParentId):
    try:
        #查詢列表
        result = dict_dao.queryDictListByDictParentId(dictParentId)
        dictList = list(map(lambda x: x.to_dict(),result))
    except:
        return 400, '根据父级字典ID获取子集字典列表发生错误!'
    restResult = RestResult(0, "OK", len(dictList), dictList)
    return jsonify(restResult.__dict__)