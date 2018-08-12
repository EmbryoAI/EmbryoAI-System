# -*- coding: utf8 -*-

from entity.RestResult import RestResult
from flask import request, jsonify
import json,os
from app import conf
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

def getWellVideo(agrs):
    import cv2

    procedure_id = agrs['procedure_id']
    dish_id = agrs['dish_id']
    well_id = agrs['well_id']

    #先获取视频保存目录
    dish = dish_mapper.queryById(dish_id)
    if not dish : 
        return None
        
    dishCode = dish.dishCode
    pd = procedure_dish_mapper.queryByProcedureIdAndDishId(procedure_id, dish_id)
    path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep  
    video_path = path + 'video'

    #判断该目录是否存在
    video_path_exists = os.path.exists(video_path)
    if not video_path_exists:
        #目录不存在则创建目录
        os.makedirs(video_path)

    video_name = video_path + os.path.sep + pd.imagePath + f'_DISH{dishCode}_{well_id}.mp4'
    print(video_name)

    fps = 5 #每秒几帧
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    videoWriter = cv2.VideoWriter(video_name,fourcc,fps,(1280,960))

    jsonPath = path + conf['DISH_STATE_FILENAME']
    with open(f'{jsonPath}', 'r') as fn :
        dishJson = json.loads(fn.read())
    seris_json = dishJson['wells'][f'{well_id}']['series']
    for series in seris_json:
        image_name = seris_json[series]['sharp']
        image_path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep + series + os.path.sep + image_name 
        frame = cv2.imread(image_path)
        frame = cv2.resize(frame,(1280,960))
        videoWriter.write(frame)
    videoWriter.release()

    cap = open(video_name,'rb').read()
    return cap
        
