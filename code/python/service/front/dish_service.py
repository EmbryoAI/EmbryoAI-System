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
import dao.front.milestone_mapper as milestone_mapper
from common import logger
from task.TimeSeries import TimeSeries,serie_to_time
from collections import OrderedDict
import dao.front.dict_dao as dict_dao
from entity.Series import Series
from entity.SeriesResult import SeriesResult
import dao.front.dish_mapper as dish_mapper
import dao.front.cell_mapper as cell_mapper

def querySeriesList(agrs):
    try:
        from common import getdefault
        procedure_id = agrs['procedure_id']
        dish_id = agrs['dish_id']
        well_id = agrs['well_id']
        seris = agrs['seris']
        last_embryo_serie = seris
        if seris == 'null':
            last_embryo_serie = ''
            seris = '0000000'
        #先查询病例对应的采集目录路径
        dish = dish_mapper.queryById(dish_id)
        if not dish : 
            return 500, f'查无对应的皿信息{dish_id}'
        dishCode = dish.dishCode
        pd = procedure_dish_mapper.queryByProcedureIdAndDishId(procedure_id,dish_id)
        path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep  
        if not os.path.isdir(path) :
            return 500, f'查无对应的采集目录{path}'
        #再拼接对应目录下面的JSON文件路径
        path,dishJson = image_service.getImagePath(procedure_id,dish_id)
        well_json = dishJson['wells'][well_id]

        #开始计算要返回的11张序列
        ts = TimeSeries()
        end_index = len(ts.range(seris)) + 6
        begin_index = len(ts.range(seris)) - 5

        #判断是否超过最后一张序列的位置
        if len(ts.range(dishJson['lastSerie'])) - len(ts.range(seris)) < 10:
            end_index = len(ts.range(dishJson['lastSerie'])) + 1
            begin_index = end_index - 11
        #判断是否第一张序列的位置
        if begin_index < 0:
                begin_index = 0
                end_index = 11

        #拼接返回的list
        nginxImageUrl = getdefault(conf, 'STATIC_NGINX_IMAGE_URL', "http://localhost:80")
        list=[]
        for i in ts[begin_index:end_index]:
            try:
                image_path = nginxImageUrl + os.path.sep + pd.imagePath + os.path.sep + f'DISH{dishCode}' + \
                os.path.sep + well_json['series'][i]['focus']
            except:
                #如果读取json中某个序列异常则默认显示定位不到胚胎图片
                image_path = '/static/front/img/loc-emb.png'
            
            hour, minute = serie_to_time(i)
            series = Series(i, f'{hour:02d}H{minute:02d}M', image_path)
            list.append(series.__dict__)

        #查询里程碑信息
        current_cell = cell_mapper.getCellByDishIdAndCellCode(dish_id, well_id)
        if not current_cell:
            500, f'查询当前孔信息异常dishId:{dish_id}cellCode{well_id}'
        embryo = embryo_mapper.queryByProcedureIdAndCellId(procedure_id, current_cell.id)
        milestone_list = milestone_mapper.getMilestone(embryo.id)
        m_list = []
        for milestone in milestone_list:
            obj={}
            obj['milestoneType'] = milestone.milestone_type
            obj['embryoId'] = milestone.embryo_id
            obj['seris'] = milestone.seris
            m_list.append(obj)
        
        if not milestone_list:
            obj={}
            obj['embryoId'] = embryo.id
            m_list.append(obj)
        seriesResult = SeriesResult(200, 'OK', list, seris, dishJson['lastSerie'], m_list, last_embryo_serie)
        return 200, jsonify(seriesResult.__dict__)
    except:
        return 500, '获取序列列表异常'

def queryScrollbarSeriesList(agrs):
    try:
        from common import getdefault
        procedure_id = agrs['procedure_id']
        dish_id = agrs['dish_id']
        well_id = agrs['well_id']
        current_seris = agrs['current_seris']
        direction = agrs['direction']

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
        logUtils.info(jsonPath)
        with open(f'{jsonPath}', 'r') as fn :
            dishJson = json.loads(fn.read())

        well_json = dishJson['wells'][well_id]

        ts = TimeSeries()

        last_serie = dishJson['lastSerie']
        if direction == 'left':
            if len(ts.range(current_seris)) < 11:
                begin_index = 0
                end_index = 11
                current_seris = ts[5]
            else:
                current_seris = ts[len(ts.range(current_seris)) - 11]
                begin_index = len(ts.range(current_seris)) - 5
                if begin_index <= 0:
                    begin_index = 0
                end_index = begin_index + 11

        if direction == 'right':
            
            current_seris = ts[len(ts.range(current_seris)) + 11]
            begin_index = len(ts.range(current_seris)) - 5
            end_index = begin_index + 11

            if end_index >= len(ts.range(last_serie)):
                end_index = len(ts.range(last_serie)) + 1
                begin_index = end_index - 11

        #拼接返回的list
        nginxImageUrl = getdefault(conf, 'STATIC_NGINX_IMAGE_URL', "http://localhost:80")
        list=[]
        for i in ts[begin_index:end_index]:
            image_path = nginxImageUrl + os.path.sep + pd.imagePath + os.path.sep + f'DISH{dishCode}' + \
                os.path.sep + well_json['series'][i]['focus']
            hour, minute = serie_to_time(i)
            series = Series(i, f'{hour:02d}H{minute:02d}M', image_path)
            list.append(series.__dict__)

        #查询里程碑信息
        current_cell = cell_mapper.getCellByDishIdAndCellCode(dish_id, well_id)
        embryo = embryo_mapper.queryByProcedureIdAndCellId(procedure_id, current_cell.id)
        milestone_list = milestone_mapper.getMilestone(embryo.id)
        m_list = []
        for milestone in milestone_list:
            obj={}
            obj['milestoneType'] = milestone.milestone_type
            obj['embryoId'] = milestone.embryo_id
            obj['seris'] = milestone.seris
            m_list.append(obj)
        
        if not milestone_list:
            obj={}
            obj['embryoId'] = embryo.id
            m_list.append(obj)

        seriesResult = SeriesResult(200, 'OK', list, current_seris, dishJson['lastSerie'], m_list, current_seris)
        return 200, jsonify(seriesResult.__dict__)
    except:
        return 500, '左右滚动查询序列列表异常'

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
        logUtils.info("根据培养箱id查询皿信息失败")
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
        return 200, jsonify(list)
    except : 
        logUtils.info("读取dishState.json文件出现异常")
        return 500, '查询序列列表异常'

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
            dictPnNum =  dict_dao.getDictByClassAndKey("pn",key["pnId"])
            if dictPnNum:
               tableObj["pnNum"] = dictPnNum.dictValue
            else:     
               tableObj["pnNum"] = 0
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
                            value = conf['EMBRYOAI_IMAGE_ROOT']+lcb[1]+","+ f'{hour:02d}H{minute:02d}M'
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