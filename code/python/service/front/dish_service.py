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
from task.TimeSeries import TimeSeries,serie_to_time


def querySeriesList(agrs):
    procedure_id = agrs['procedure_id']
    dish_id = agrs['dish_id']
    well_id = agrs['well_id']
    seris = agrs['seris']

    try :
        dish = dish_mapper.queryById(dish_id)
        if not dish : 
            return None
            
        dishCode = dish.dishCode
        pd = procedure_dish_mapper.queryByProcedureIdAndDishId(procedure_id,dish_id)
        path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep  
        if not os.path.isdir(path) :
            return None
            
        # E:\EmbryoAI\EmbryoAI-System\code\captures\20180422152100\DISH8\dish_state.json
        jsonPath = path + conf['DISH_STATE_FILENAME']
        logger().info(jsonPath)
        with open(f'{jsonPath}', 'r') as fn :
            dishJson = json.loads(fn.read())

        well_json = dishJson['wells'][well_id]
        last_seris = well_json['lastEmbryoSerie']
        print(last_seris)

        if seris != 'lastEmbryoSerie':
            last_seris = seris
        

        ts = TimeSeries()
        last_index = len(ts.range(last_seris)) + 5
        begin_index = len(ts.range(last_seris)) - 4
        list=[]
        for i in ts[begin_index:last_index]:
            list.append(i)
            image_path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep + well_json['series'][i]['focus']
            list.append(image_path)
            hour, minute = serie_to_time(i)
            list.append(f'{hour:02d}H{minute:02d}M')
            list.append(last_seris)

        return jsonify(list)
    except : 
        logger().info("读取dishState.json文件出现异常")
        return None

def queryScrollbarSeriesList(agrs):
    procedure_id = agrs['procedure_id']
    dish_id = agrs['dish_id']
    well_id = agrs['well_id']
    current_seris = agrs['current_seris']
    direction = agrs['direction']

    try :
        dish = dish_mapper.queryById(dish_id)
        if not dish : 
            return None
            
        dishCode = dish.dishCode
        pd = procedure_dish_mapper.queryByProcedureIdAndDishId(procedure_id,dish_id)
        path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep  
        if not os.path.isdir(path) :
            return None
            
        # E:\EmbryoAI\EmbryoAI-System\code\captures\20180422152100\DISH8\dish_state.json
        jsonPath = path + conf['DISH_STATE_FILENAME']
        logger().info(jsonPath)
        with open(f'{jsonPath}', 'r') as fn :
            dishJson = json.loads(fn.read())

        well_json = dishJson['wells'][well_id]

        ts = TimeSeries()
        last_index = len(ts.range(current_seris)) + 5
        begin_index = len(ts.range(current_seris)) - 4

        if direction == 'left':
            last_index = last_index - 9
            begin_index = begin_index - 9
        if direction == 'right':
            last_index = last_index + 9
            begin_index = begin_index + 9

        list=[]
        for i in ts[begin_index:last_index]:
            list.append(i)
            image_path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep + well_json['series'][i]['focus']
            list.append(image_path)
            hour, minute = serie_to_time(i)
            list.append(f'{hour:02d}H{minute:02d}M')
            list.append(current_seris)

        return jsonify(list)
    except : 
        logger().info("读取dishState.json文件出现异常")
        return None
