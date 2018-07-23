# -*- coding: utf8 -*-

from entity.RestResult import RestResult
import dao.front.embryo_mapper as embryo_mapper
from flask import request, jsonify
import json
from app import conf
import service.front.image_service as image_service



def queryWellList(procedureId, dishId):
    path, well_json = image_service.readDishState(procedureId, dishId)
    list=[]
    for key in well_json['wells']:
        list.append(key)
        print(well_json['wells'][key]['series']['0000000']['focus'])
    return jsonify(list)

   
