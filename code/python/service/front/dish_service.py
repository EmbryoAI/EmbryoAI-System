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
from collections import OrderedDict
import dao.front.dict_dao as dict_dao
from entity.Series import Series
from entity.SeriesResult import SeriesResult

def querySeriesList(agrs):
    procedure_id = agrs['procedure_id']
    dish_id = agrs['dish_id']
    well_id = agrs['well_id']
    seris = agrs['seris']
    cell_id = agrs['cell_id']

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

        if seris != 'lastEmbryoSerie':
            last_seris = seris
        

        ts = TimeSeries()
        last_index = len(ts.range(last_seris)) + 5
        begin_index = len(ts.range(last_seris)) - 4

        if begin_index < 0:
            begin_index = 0
            last_index = 9

        if last_index - len(ts.range(dishJson['lastSerie'])) > 0:
            last_index = len(ts.range(dishJson['lastSerie']))
            begin_index = last_index - 9

        #list=[]
        #for i in ts[begin_index:last_index]:
        #    list.append(i)
        #    image_path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep + well_json['series'][i]['focus']
        #    list.append(image_path)
        #    hour, minute = serie_to_time(i)
        #    list.append(f'{hour:02d}H{minute:02d}M')
        #    list.append(last_seris)
        
        list=[]
        for i in ts[begin_index:last_index]:
            image_path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep + well_json['series'][i]['focus']
            hour, minute = serie_to_time(i)
            series = Series(i, f'{hour:02d}H{minute:02d}M', image_path)
            list.append(series.__dict__)

        #查询胚胎id
        embryo = embryo_mapper.queryByProcedureIdAndCellId(procedure_id, cell_id)

        seriesResult = SeriesResult(200, 'OK', list, last_seris, embryo.id)

        return jsonify(seriesResult.__dict__)
    except : 
        logger().info("读取dishState.json文件出现异常")
        seriesResult = SeriesResult(400, '获取序列出现异常', None, None, None)
        return jsonify(seriesResult.__dict__)

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

        last_serie = dishJson['lastSerie']

        if direction == 'left':
            if len(ts.range(current_seris)) < 9:
                begin_index = 0
                last_index = 9
                current_seris = ts[4]
            else:
                print(len(ts.range(current_seris)))
                current_seris = ts[len(ts.range(current_seris)) - 9]
                begin_index = len(ts.range(current_seris)) - 4
                last_index = begin_index + 9

        if direction == 'right':
            
            current_seris = ts[len(ts.range(current_seris)) + 9]
            begin_index = len(ts.range(current_seris)) - 4
            last_index = begin_index + 9

            if last_index >= len(ts.range(last_serie)):
                last_index = len(ts.range(last_serie))
                begin_index = last_index - 9
                current_seris = ts[len(ts.range(last_serie)) - 4]

        list=[]
        for i in ts[begin_index:last_index]:
            image_path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep + well_json['series'][i]['focus']
            hour, minute = serie_to_time(i)
            series = Series(i, f'{hour:02d}H{minute:02d}M', image_path)
            list.append(series.__dict__)

        seriesResult = SeriesResult(200, 'OK', list, current_seris, None)

        return jsonify(seriesResult.__dict__)
    except : 
        logger().info("读取dishState.json文件出现异常")
        seriesResult = SeriesResult(400, '获取序列出现异常', None, None, None)
        return jsonify(seriesResult.__dict__)



def loadDishByIncubatorId(agrs):
    incubatorId = agrs["incubatorId"]
    procedureId = agrs["procedureId"]
    try :
        if not incubatorId :
            return 401, '培养箱id不能为空!'
        imagePath = getImagePath(incubatorId,procedureId)
        params = {'incubatorId': incubatorId,'imagePath': imagePath}
        result = dish_mapper.findDishByIncubatorId(params)
        dishList = list(map(dict, result))
        restResult = RestResult(200, "OK", len(dishList), dishList)
        return jsonify(restResult.__dict__)
    except :
        logger().info("根据培养箱id查询皿信息失败")
        return 400, '根据培养箱id查询皿信息失败!'
    
'''
    根据周期id或培养箱id获取采集目录：
    周期id不为空时，根据周期id查询采集目录。一个周期id只有一个采集目录
    周期id为空时，根据培养箱id获取最新的采集目录
'''
def getImagePath(incubatorId,procedureId):
    if not procedureId.strip():
        imagePath = dish_mapper.findLatestImagePath(incubatorId)
    else :
        imagePath = dish_mapper.findImagePathByProcedureId(procedureId)
    return imagePath    

def getSeriesList(agrs):
    procedureId = agrs['procedureId']
    dishId = agrs['dishId']
    wellId = agrs['wellId']

    try :
        imagePath,path,dishJson = image_service.readDishState(procedureId,dishId)
        list=[]
        if dishJson is not None:
            well_json = dishJson['wells'][wellId]
            series = well_json["series"]
            for key in series:
                obj = {}
                obj["serie"] = key
                hour, minute = serie_to_time(key)
                obj["showTime"] = f'{hour:02d}H{minute:02d}M'
                list.append(obj)
        return jsonify(list)
    except : 
        logger().info("读取dishState.json文件出现异常")
        return None

"""根据皿ID获取胚胎评分表"""
def emGrade(dishId):
    try:
        emGradeList = dish_mapper.emGrade(dishId)
        emGradeList = list(map(dict, emGradeList))
        return 200,emGradeList
    except:
        return 400,"根据皿ID获取胚胎评分表失败"


"""根据皿ID获取胚胎总览表"""
def emAll(dishId):
    try:
         #查询字典表里程碑的节点
        result = dict_dao.queryDictListByClass("milestone")
        dictList = list(map(lambda x: x.to_dict(),result))
        
        procedureViewList=[]
        #表格的动态头
        tableObj=OrderedDict()
        tableObj["codeIndex"] = "编号"
        tableObj["pnNum"] = "PN数"
        for key in dictList:
            tableObj[key['dictValue']] = key['dictValue']
        tableObj["embryoFate"] = "结局"
        procedureViewList.append(tableObj)
        
                #查詢列表
        procedureList = dish_mapper.emAll(dishId)
     
        #循环查询出来的值
        for key in procedureList:
            tableObj=OrderedDict()
            tableObj["codeIndex"] = key["codeIndex"]
            pnNum =  dict_dao.getDictByClassAndKey("pn",key["pnId"])
            tableObj["pnNum"] = pnNum
            #如果里程碑字段不为空
            if key['lcb']!=None:
                #由于使用mysql GROUP_CONCAT函数 行转列 需要截取
                lcbstr = key['lcb'].split(",")
                for dictObj in dictList:
                    value = ""
                    for lcbjd in lcbstr:
                        lcb = lcbjd.split("#")
                        if dictObj['dictValue'] == lcb[0]: #如果相等的话
                            hour, minute = serie_to_time(lcb[2])
                            value = lcb[1]+","+ f'{hour:02d}H{minute:02d}M'
                            break
                    tableObj[dictObj['dictValue']] = value
            else:
                for dictObj in dictList:
                    tableObj[dictObj['dictValue']] = ""
            tableObj["embryoFate"] = key["embryoFate"]
            procedureViewList.append(tableObj)
        
        
        return 200,procedureViewList
    except:
        return 400,"根据皿ID获取胚胎总览表失败"                                                                                               