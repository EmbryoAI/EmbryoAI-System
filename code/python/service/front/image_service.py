# -*- coding: utf8 -*-
from entity.RestResult import RestResult
import dao.front.procedure_dish_mapper as procedure_dish_mapper
import dao.front.dish_mapper as dish_mapper
import entity.ProcedureDish as ProcedureDish
import entity.Dish as Dish
from flask import request, jsonify
from common import uuid,logger
from app import conf
import json,os

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
                zData['path'] = path
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
        # if dishJson['finished'] & dishJson['avail'] == 1 :
        #     return pd.imagePath,path, dishJson
        # else :
        #     return None,None,None
        return pd.imagePath,path, dishJson
    except : 
        logger().info("读取dishState.json文件出现异常")
        return None,None,None


def markDistinct(agrs):
    import cv2
    from task.process_serie_dir import read_img_grayscale
    from cv.embryo_detector import find_embryo
    from cv.embryo_common import outer_edge,cell_edge
    from task.dish_config import DishConfig,SerieInfo
    from common import nested_dict
    logger().info(agrs)
    wellId = agrs['wellId']
    path = agrs['path']
    imageName = agrs['imageName']
    timeSeries = agrs['timeSeries']
    
    try :
        dishJsonPath = path + conf['DISH_STATE_FILENAME']
        with open(dishJsonPath) as fn:
            jstr = json.load(fn)
            dishConf = DishConfig(jstr)
        imagePath = path + timeSeries + os.path.sep + imageName
        if imagePath :
            serieInfo = dishConf.wells[wellId].series[timeSeries]
            logger().info(nested_dict(serieInfo))
            img = read_img_grayscale(imagePath)
            # 定位胚胎位置
            left, top, right, bottom = find_embryo(img)
            imgFocus = img[top:bottom, left:right]
            # focusPath = path + conf['EMBRYO_FOCUS_DIRNAME'] + os.path.sep
            # if not os.path.exists(focusPath):
            #     os.makedirs(focusPath)
            focusFile = serieInfo.focus  
            print(path + focusFile)
            # if os.path.exists(focusPath + focusFile):
            #     os.remove(focusPath + focusFile)
            # 保存缩略图
            cv2.imwrite(path + focusFile, imgFocus, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            outer_cnt, outer_area, outer_diameter = outer_edge(imgFocus)
            if len(outer_cnt):
                serieInfo.outerArea = outer_area
                serieInfo.outerDiameter = outer_diameter
            cell_result = cell_edge(imgFocus)
            if len(cell_result) == 1:
                serieInfo.innerArea = cell_result[0][1]
                serieInfo.innerDiameter = cell_result[0][2]
            if len(cell_result) == 2:
                serieInfo.innerArea = cell_result[0][1]
                serieInfo.innerDiameter = cell_result[0][2]
                serieInfo.expansionArea = cell_result[1][1]
            if serieInfo.outerDiameter and serieInfo.innerDiameter \
                    and serieInfo.outerDiameter > serieInfo.innerDiameter:
                serieInfo.zonaThickness = (serieInfo.outerDiameter - serieInfo.innerDiameter) * 0.425
            
            serieInfo.sharp = imageName
            dishConf.wells[wellId].series[timeSeries] = serieInfo

            logger().info(nested_dict(dishConf.wells[wellId].series[timeSeries]))
            with open(dishJsonPath, 'w') as fn:
                fn.write(json.dumps(nested_dict(dishConf)))
            restResult = RestResult(200, "标记最清晰图片成功", 0, imageName)
    except:
        restResult = RestResult(404, "标记最清晰图片错误", 0, imageName)
    return jsonify(restResult.__dict__)