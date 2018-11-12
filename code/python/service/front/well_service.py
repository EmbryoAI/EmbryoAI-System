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

    import dao.front.embryo_mapper as embryo_mapper
    from entity.Well import Well
    from entity.WellResult import WellResult
    import dao.front.milestone_mapper as milestone_mapper

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
    with open(f'{jsonPath}', 'r') as fn :
        dishJson = json.loads(fn.read())
    

    #先查询该皿ID下面的所有孔数据
    cell_list = cell_mapper.queryCellByDishId(dishId)

    well_list=[]
    for key in dishJson['wells']:
        last_embryo_seris = dishJson['wells'][key]['lastEmbryoSerie']
        image_path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + \
            os.path.sep + dishJson['wells'][key]['series'][last_embryo_seris]['focus']

        cell_id = ""
        #再跟JSON里面的序列匹配孔ID
        for cell in cell_list:
            if key == cell.cell_code:
                cell_id = cell.cell_id

        well = Well(key, image_path, cell_id, last_embryo_seris)
        well_list.append(well.__dict__)

    #查询里程碑信息
    embryo = embryo_mapper.queryByProcedureIdAndCellId(procedureId, cell_id)
    milestone_list = milestone_mapper.getMilestone(embryo.id)
    list = []
    for milestone in milestone_list:
        print('milestone:',milestone)
        obj={}
        obj['milestoneType'] = milestone.milestone_type
        obj['embryoId'] = milestone.embryo_id
        obj['seris'] = milestone.seris
        list.append(obj)

    wellResult = WellResult(200, 'OK', well_list, list, dishJson['lastSerie'])

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

    video_name = video_path + os.path.sep + pd.imagePath + f'_DISH{dishCode}_{well_id}.webm'
    print(video_name)

    font_name = ImageFont.truetype('NotoSansCJK-Black.ttc', 30)
    font_time = ImageFont.truetype('NotoSansCJK-Black.ttc', 20)
    color = (0, 0, 0)

    fps = 5 #每秒几帧
    fourcc = cv2.VideoWriter_fourcc(*'WEBM')
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

def getWellVideoPath(agrs):
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

    video_exists = os.path.exists(video_name)
    if not video_exists:
        font_name = ImageFont.truetype('NotoSansCJK-Black.ttc', 30)
        font_time = ImageFont.truetype('NotoSansCJK-Black.ttc', 20)
        color = (0, 0, 0)

        fps = 5 #每秒几帧
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
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
    download_path = conf['STATIC_NGINX_IMAGE_URL'] + os.path.sep + pd.imagePath + os.path.sep \
             + f'DISH{dishCode}' + os.path.sep  + 'video' + os.path.sep + pd.imagePath + f'_DISH{dishCode}_{well_id}.mp4'
    return jsonify(download_path)

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

#查询采集目录
def queryCollectionCatalog():
    json_path = conf['EMBRYOAI_IMAGE_ROOT'] + conf['FINISHED_CYCLES']
    with open(f'{json_path}', 'r') as fn :
        catalog_json = json.loads(fn.read())
    #读取FINISHED_CYCLES JSON文件中所有的采集目录并存放到set中
    all_relation_catalog_set = set()    
    for catalog in catalog_json:
        for key in catalog:
            all_relation_catalog_set.add(key)
    #读取数据库中已关联的采集目录并存放到set中
    relation_catalogs = procedure_dish_mapper.queryAllCatalog()
    relation_catalog_set = set()  
    for rc in relation_catalogs:
        relation_catalog_set.add(rc.relation_catalog)
    #将两个set做difference操作得到未关联的采集目录返回前端
    no_relation_catalog = all_relation_catalog_set.difference(relation_catalog_set)

    return jsonify(list(no_relation_catalog))

#查询采集目录详情,包括目录下的培养箱,培养皿,用户姓名,开始采集时间,胚胎数量等
def getCollectionCatalogInfo(agrs):
    from task.ini_parser import EmbryoIniParser as parser
    from entity.Catalog import Catalog
    from common import parse_time_for_date_str

    catalog_name = agrs['catalogName']
    try:
        #拼接ini文件路径
        ini_path = conf['EMBRYOAI_IMAGE_ROOT'] + os.path.sep + catalog_name + os.path.sep + 'DishInfo.ini'
        #解析ini文件
        config = parser(ini_path)
        #获取培养箱信息
        incubator_name = config['IncubatorInfo']['IncubatorName']
        #获取培养皿信息
        dish_list = []
        dishes = [f'Dish{i}Info' for i in range(1, 10) if f'Dish{i}Info' in config]
        for dish in dishes:
            dish_list.append(dish[0:5])
        #获取患者姓名
        patient_name = config[dishes[0]]['PatientName']
        #获取采集开始时间
        collection_date = config['Timelapse']['StartTime']
        collection_date = parse_time_for_date_str(collection_date)
        #获取胚胎数量
        wells = [f'Well{i}Avail' for i in range(1, 13)]
        embryo_number = len([index for d in dishes for index,w in enumerate(wells) if config[d][w]=='1'])

        #封装成对象返回前端
        catalog = Catalog(incubator=incubator_name, dish_list=dish_list, patient_name=patient_name, \
                collection_date=collection_date, embryo_number=embryo_number)

        result = RestResult(code=200, msg='查询采集目录信息成功', count=None, data=catalog.__dict__)

        return jsonify(result.__dict__)
    except:
        result = RestResult(code=500, msg='查询采集目录信息异常', count=None, data=None)
        return jsonify(result.__dict__)