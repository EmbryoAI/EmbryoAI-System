# -*- coding: utf8 -*-

from entity.RestResult import RestResult
import dao.front.embryo_mapper as embryo_mapper
from flask import request, jsonify



def queryEmbryoList(id):
    result = embryo_mapper.queryEmbryoList(id)
    restResult = RestResult(0, "OK", len(result), list(map(dict, result)))
    return jsonify(restResult.__dict__)
