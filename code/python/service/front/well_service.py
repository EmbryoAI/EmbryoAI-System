# -*- coding: utf8 -*-

from entity.RestResult import RestResult
import dao.front.embryo_mapper as embryo_mapper
from flask import request, jsonify
import json,os
from app import conf
import service.front.image_service as image_service
import base64
import dao.front.dish_mapper as dish_mapper
import dao.front.procedure_dish_mapper as procedure_dish_mapper
from common import logger
from task.TimeSeries import TimeSeries


def queryWellList(procedureId, dishId):
    try :
        dish = dish_mapper.queryById(dishId)
        if not dish : 
            return None
            
        dishCode = dish.dishCode
        pd = procedure_dish_mapper.queryByProcedureIdAndDishId(procedureId,dishId)
        path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep  
        if not os.path.isdir(path) :
            return None
            
        # E:\EmbryoAI\EmbryoAI-System\code\captures\20180422152100\DISH8\dish_state.json
        jsonPath = path + conf['DISH_STATE_FILENAME']
        logger().info(jsonPath)
        with open(f'{jsonPath}', 'r') as fn :
            dishJson = json.loads(fn.read())
        list=[]
        for key in dishJson['wells']:
            list.append(key)
            last_seris = dishJson['wells'][key]['lastEmbryoSerie']
            image_path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep + dishJson['wells'][key]['series'][last_seris]['focus']
            list.append(image_path)
        return jsonify(list)
    except : 
        logger().info("读取dishState.json文件出现异常")
        return None

def getWellImage(agrs):
    image_path = agrs['image_path']
    image = open(image_path,'rb').read()
    return image

def getPreFrame(agrs):
    current_seris = agrs['current_seris']
    ts = TimeSeries()
    pre_index = len(ts.range(current_seris)) - 1
    return ts[pre_index]

def getNextFrame(agrs):
    current_seris = agrs['current_seris']
    ts = TimeSeries()
    ts.move_to(len(ts.range(current_seris)) + 1)
    return ts.next()