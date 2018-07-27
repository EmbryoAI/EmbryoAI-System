# -*- coding: utf8 -*-
from entity.RestResult import RestResult
import dao.front.dict_dao as dict_dao
from flask import request, jsonify
from common import uuid
import json

def queryDictListByClass(dictClass):
    try:
        #查詢列表
        result = dict_dao.queryDictListByClass(dictClass)
        dictList = list(map(lambda x: x.to_dict(),result))
    except:
        return 400, '查询字典列表时发生错误!'
    restResult = RestResult(0, "OK", len(dictList), dictList)
    return jsonify(restResult.__dict__)


def queryDictListByClassS(dictClass):
    try:
        #查詢列表
        result = dict_dao.queryDictListByClassS(dictClass)
        dictList = list(map(lambda x: x.to_dict(),result))
    except:
        return 400, '查询字典列表时发生错误!'
    restResult = RestResult(0, "OK", len(dictList), dictList)
    return jsonify(restResult.__dict__)