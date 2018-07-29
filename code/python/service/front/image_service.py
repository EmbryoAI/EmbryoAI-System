# -*- coding: utf8 -*-
from entity.RestResult import RestResult
import dao.front.procedure_dish_mapper as procedure_dish_mapper
import dao.front.dish_mapper as dish_mapper
import entity.ProcedureDish as ProcedureDish
import entity.Dish as Dish
from flask import request, jsonify
from common import uuid,logger
from app import conf
import json,os,cv2

def getImageByCondition(agrs):
    logger().info(agrs)
    procedureId = agrs['procedureId']
    dishId = agrs['dishId']
    wellId = agrs['wellId']
    timeSeries = agrs['timeSeries']
    zIndex = agrs['zIndex']
    try:
        imagePath,path,dishJson = readDishState(procedureId,dishId)
        if dishJson['finished'] & dishJson['avail'] == 1 : 
            if not timeSeries.strip() :
            # if not timeSeries:
                timeSeries = dishJson['lastSerie']
            wells = dishJson['wells']
            oneWell = wells[f'{wellId}']
            series = oneWell['series']
            oneSeries = series[f'{timeSeries}']
            jpgName = oneSeries['sharp']
            # jpgName = oneSeries['focus']
            if zIndex :
                zIndexFiles = oneWell['zIndexFiles']
                jpgName = zIndexFiles[f'{zIndex}']
            jpgPath = path + timeSeries + os.path.sep + jpgName
            logger().info(jpgPath)
            # image = cv2.imread(r'e:\EmbryoAI\EmbryoAI-System\code\python\..\captures\20180422152100\DISH8\7000000\00006.jpg')
            image = open(jpgPath,'rb').read()
        else :
            logger("文件未处理完成或皿状态是无效的")
            image = None
    except:
        logger().info("获取图片文件出现异常")
        image = None
    return image

def getAllZIndex(agrs):
    procedureId = agrs['procedureId']
    dishId = agrs['dishId']
    wellId = agrs['wellId']
    timeSeries = agrs['timeSeries']
    zData = {}
    try:
        imagePath,path,dishJson = readDishState(procedureId,dishId)
        if dishJson['finished'] & dishJson['avail'] == 1 : 
            wells = dishJson['wells']
            oneWell = wells[f'{wellId}']
            if oneWell['avail']:
                zData['imagePath'] = imagePath
                zData['zIndexFiles'] = oneWell['zIndexFiles']
                zData['zcount'] = oneWell['zcount']
                zData['zslice'] = oneWell['zslice']
                zData['fileStart'] = oneWell['fileStart']
                zData['fileEnd'] = oneWell['fileEnd']
            # if not timeSeries :
            if not timeSeries.strip() :
                timeSeries = dishJson['lastSerie']
            series = oneWell['series']
            oneSeries = series[f'{timeSeries}']
            zData['sharp'] = oneSeries['sharp']
        logger().info(zData)
        restResult = RestResult(200, "获取所有z轴节点成功", 1, dict(zData))
    except:
        logger().info("获取所有z轴节点失败")
        restResult = RestResult(404, "获取该时间序列下的所有z轴节点失败", 0, None)
    return jsonify(restResult.__dict__)


def readDishState(procedureId,dishId):
    try :
        dish = dish_mapper.queryById(dishId)
        if not dish : 
            return None
        dishCode = dish.dishCode
        pd = procedure_dish_mapper.queryByProcedureIdAndDishId(procedureId,dishId)
        path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep  
        if not os.path.isdir(path) :
            return None,None
        # E:\EmbryoAI\EmbryoAI-System\code\captures\20180422152100\DISH8\dish_state.json
        jsonPath = path + conf['DISH_STATE_FILENAME']
        logger().info(jsonPath)
        with open(f'{jsonPath}', 'r') as fn :
            dishJson = json.loads(fn.read())
        if dishJson['finished'] & dishJson['avail'] == 1 :
            return pd.imagePath,path, dishJson
        else :
            return None,None,None
    except : 
        logger().info("读取dishState.json文件出现异常")
        return None,None,None