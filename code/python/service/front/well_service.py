# -*- coding: utf8 -*-

from entity.RestResult import RestResult
from flask import request, jsonify
import json,os
from app import conf
import base64
import dao.front.dish_mapper as dish_mapper
import dao.front.cell_mapper as cell_mapper
import dao.front.procedure_dish_mapper as procedure_dish_mapper
import dao.front.incubator_mapper as incubator_mapper
import dao.front.procedure_mapper as procedure_mapper

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

        
        from entity.Well import Well
        from entity.WellResult import WellResult
        list=[]
        for key in dishJson['wells']:
            last_seris = dishJson['wells'][key]['lastEmbryoSerie']
            image_path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep + dishJson['wells'][key]['series'][last_seris]['focus']
            cell = cell_mapper.getCellByDishIdAndCellCode(dishId, key)
            if not cell:
                logger().info("查询孔数据异常")
                return None
            well = Well(key, image_path, cell.id)
            list.append(well.__dict__)

        wellResult = WellResult(200, 'OK', list)

        return jsonify(wellResult.__dict__)
    except : 
        logger().info("读取dishState.json文件出现异常")
        wellResult = WellResult(400, 'FAIL', None)
        return jsonify(wellResult.__dict__)

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
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    from task.TimeSeries import serie_to_time

    procedure_id = agrs['procedure_id']
    procedure_result = procedure_mapper.getProcedureById(procedure_id)
    patient_name = procedure_result['patient_name']
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

    font_name = ImageFont.truetype('NotoSansCJK-Black.ttc', 30)
    font_time = ImageFont.truetype('NotoSansCJK-Black.ttc', 20)
    color = (0, 0, 0)

    fps = 5 #每秒几帧
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    videoWriter = cv2.VideoWriter(video_name,fourcc,fps,(1280,960))

    jsonPath = path + conf['DISH_STATE_FILENAME']
    with open(f'{jsonPath}', 'r') as fn :
        dishJson = json.loads(fn.read())
    seris_json = dishJson['wells'][f'{well_id}']['series']
    for series in seris_json:
        image_name = seris_json[series]['sharp']
        image_path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep \
            + f'DISH{dishCode}' + os.path.sep + series + os.path.sep + image_name 
        frame = cv2.imread(image_path)
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)
        draw.text((50, 10), patient_name, font=font_name, fill=color)
        hour, minute = serie_to_time(series)
        draw.text((1150, 10), f'{hour:02d} H {minute:02d} M', font=font_time, fill=color)
        # if seris_json[series]['stage']:
            # draw.text((1150, 30), seris_json[series]['stage'], font=font_time, fill=color)
        frame = np.asarray(img_pil)

        # frame = cv2.resize(frame,(1280,960))

        videoWriter.write(frame)
    videoWriter.release()

    cap = open(video_name,'rb').read()
    return cap

#查询培养箱
def queryIncubator():
    json_path = conf['EMBRYOAI_IMAGE_ROOT'] + conf['FINISHED_CYCLES']
    with open(f'{json_path}', 'r') as fn :
        catalog_json = json.loads(fn.read())

    list = []
    for catalog in catalog_json:
        catalog_path = conf['EMBRYOAI_IMAGE_ROOT'] + catalog
        dirs = os.listdir(catalog_path)
        for dir in dirs:
            dish_path = catalog_path + os.path.sep + dir
            if os.path.isdir(dish_path):  
                if dir[0] == '.':  
                    pass  
                else:  
                    dish_json_path = dish_path + os.path.sep + conf['DISH_STATE_FILENAME']
                    with open(f'{dish_json_path}', 'r') as dn :
                        dish_json = json.loads(dn.read())
                    incubator_name = dish_json['incubatorName']
                    #先查询该培养箱是否被关联，如果没被关联则直接返回
                    incubator = incubator_mapper.getByIncubatorCode(incubator_name)
                    if not incubator:
                        list.append(incubator_name)
                    #如果关联了则查询该培养箱下面的培养皿是否全部被关联
                    else:
                        dish_code = dir[4:5]
                        dish = dish_mapper.getByIncubatorIdDishCode(incubator.id, dish_code)
                        if not dish:
                            list.append(incubator_name)
                    print(incubator_name) 
    result_list = []
    for i in list:
        if i not in result_list:
            result_list.append(i)
    return jsonify(result_list)

#查询培养皿
def queryDish(agrs):
    incubatorName = agrs['incubatorName']

    json_path = conf['EMBRYOAI_IMAGE_ROOT'] + conf['FINISHED_CYCLES']
    with open(f'{json_path}', 'r') as fn :
        catalog_json = json.loads(fn.read())

    list = []
    for catalog in catalog_json:
        catalog_path = conf['EMBRYOAI_IMAGE_ROOT'] + catalog
        dirs = os.listdir(catalog_path)
        for dir in dirs:
            dish_path = catalog_path + os.path.sep + dir
            if os.path.isdir(dish_path):  
                if dir[0] == '.':  
                    pass  
                else:  
                    dish_json_path = dish_path + os.path.sep + conf['DISH_STATE_FILENAME']
                    with open(f'{dish_json_path}', 'r') as dn :
                        dish_json = json.loads(dn.read())
                    incubator_name = dish_json['incubatorName']
                    if incubator_name == incubatorName:
                        dish_code = dir[4:5]
                        incubator = incubator_mapper.getByIncubatorCode(incubator_name)
                        if not incubator:
                            list.append(dir)
                            list.append(catalog)
                        else:
                            dish = dish_mapper.getByIncubatorIdDishCode(incubator.id, dish_code)
                            if not dish:
                                list.append(dir)
                                list.append(catalog)
                        
    return jsonify(list)
