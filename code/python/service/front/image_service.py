# -*- coding: utf8 -*-
from entity.RestResult import RestResult
import dao.front.procedure_dish_mapper as procedure_dish_mapper
import dao.front.dish_mapper as dish_mapper
import entity.ProcedureDish as ProcedureDish
import entity.Dish as Dish
from flask import request, jsonify
from common import uuid
from app import conf
import json,os
import traceback
import logUtils
from task.TimeSeries import TimeSeries,serie_to_time

def getImageByCondition(agrs):
    logUtils.info(agrs)
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
            logUtils.info(jpgPath)
            # image = cv2.imread(r'e:\EmbryoAI\EmbryoAI-System\code\python\..\captures\20180422152100\DISH8\7000000\00006.jpg')
            if os.path.exists(jpgPath) :
                image = open(jpgPath,'rb').read()
            else :
                logUtils.info("图片不存在")
                image = None
        else :
            logUtils.info("文件未处理完成或皿状态是无效的")
            image = None
    except:
        logUtils.info("获取图片文件出现异常")
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
        logUtils.info(zData)
        restResult = RestResult(200, "获取所有z轴节点成功", 1, dict(zData))
    except:
        logUtils.info("获取所有z轴节点失败")
        restResult = RestResult(404, "获取该时间序列下的所有z轴节点失败", 0, None)
    return jsonify(restResult.__dict__)

"""获取全路径"""
def readDishState(procedureId,dishId):
    try :
        dish = dish_mapper.queryById(dishId)
        if not dish : 
            return None
        dishCode = dish.dishCode
        pd = procedure_dish_mapper.queryByProcedureIdAndDishId(procedureId,dishId)
        path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep  
        if not os.path.isdir(path) :
            logUtils.info("培养皿路径不存在")
            return None,None,None
        # E:\EmbryoAI\EmbryoAI-System\code\captures\20180422152100\DISH8\dish_state.json
        jsonPath = path + conf['DISH_STATE_FILENAME']

        if os.path.exists(f'{jsonPath}') :
            with open(f'{jsonPath}', 'r') as fn :
                dishJson = json.loads(fn.read())
            if dishJson['finished'] & dishJson['avail'] == 1 :
                return pd.imagePath,path, dishJson
            else :
                logUtils.info("读取dishState.json文件,此皿为无效状态")
                return pd.imagePath,path,None
        else :
            logUtils.info("dishState.json文件不存在")
            return pd.imagePath,path,None
        
    except : 
        logUtils.info("读取dishState.json文件出现异常")
        return None,None,None

"""获取相对路径"""
def getImagePath(procedureId,dishId):
    try :
        dish = dish_mapper.queryById(dishId)
        if not dish : 
            return None,None
        dishCode = dish.dishCode
        pd = procedure_dish_mapper.queryByProcedureIdAndDishId(procedureId,dishId)
        path = conf['EMBRYOAI_IMAGE_ROOT'] + pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep  
        newPath = pd.imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep  
        if not os.path.isdir(path) :
            return None,None
        # E:\EmbryoAI\EmbryoAI-System\code\captures\20180422152100\DISH8\dish_state.json
        jsonPath = path + conf['DISH_STATE_FILENAME']
        logUtils.info(jsonPath)

        if os.path.exists(jsonPath) : 
            with open(f'{jsonPath}', 'r') as fn :
                dishJson = json.loads(fn.read())
        else :
            logUtils.info(f'文件不存在:{jsonPath}')
            return newPath,None
        if dishJson['finished'] & dishJson['avail'] == 1 :
            return newPath, dishJson
        else :
            logUtils.info(f"DISH{dishCode}未处理完成或无效")
            return newPath,None
    except : 
        logUtils.info("读取dishState.json文件出现异常")
        return None,None


def markDistinct(agrs):
    import cv2
    from task.process_serie_dir import read_img_grayscale
    from cv.embryo_detector import find_embryo
    from cv.embryo_common import outer_edge,cell_edge
    from task.dish_config import DishConfig,SerieInfo
    from common import nested_dict
    logUtils.info(agrs)
    wellId = agrs['wellId']
    path = agrs['path']
    imageName = agrs['imageName']
    timeSeries = agrs['timeSeries']
    
    try :
        dishJsonPath = path + conf['DISH_STATE_FILENAME']
        if os.path.exists(dishJsonPath) : 
            with open(dishJsonPath) as fn:
                jstr = json.load(fn)
                dishConf = DishConfig(jstr)
        
        imagePath = path + timeSeries + os.path.sep + imageName
        if os.path.exists(imagePath) and dishConf is not None :
            serieInfo = dishConf.wells[wellId].series[timeSeries]
            logUtils.info(nested_dict(serieInfo))
            img = read_img_grayscale(imagePath)
            # 定位胚胎位置
            left, top, right, bottom = find_embryo(img)
            imgFocus = img[top:bottom, left:right]
            # focusPath = path + conf['EMBRYO_FOCUS_DIRNAME'] + os.path.sep
            # if not os.path.exists(focusPath):
            #     os.makedirs(focusPath)
            focusFile = serieInfo.focus  
            logUtils.info(path + focusFile)
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

            logUtils.info(nested_dict(dishConf.wells[wellId].series[timeSeries]))
            with open(dishJsonPath, 'w') as fn:
                fn.write(json.dumps(nested_dict(dishConf)))
            restResult = RestResult(200, "标记最清晰图片成功", 0, imageName)
        else :
            restResult = RestResult(400, "标记最清晰图片失败，请联系管理员或稍后再试", 0, imageName)
    except Exception as e :
        traceback.print_exc()
        restResult = RestResult(404, "标记最清晰图片错误", 0, imageName)
    return jsonify(restResult.__dict__)


"""
根据周期ID和皿编号查询病历最新缩略图路径
"""
def getImageFouce(procedureId,dishCode):
    logUtils.info("procedureId:[%s],dishCode:[%s]"%(procedureId,dishCode))
    try:
        wellCode,imagePath = dish_mapper.queryWellIdAndImagePath(procedureId,dishCode)
        if wellCode is not None and imagePath is not None:
            # E:\EmbryoAI\EmbryoAI-System\code\captures\20180422152100\DISH8\dish_state.json
            jsonPath = conf['EMBRYOAI_IMAGE_ROOT'] + imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep + conf['DISH_STATE_FILENAME']
            if os.path.exists(jsonPath) :
                with open(f'{jsonPath}', 'r') as fn :
                    dishJson = json.loads(fn.read())
                if dishJson['finished'] & dishJson['avail'] == 1 : 
                    wells = dishJson['wells']
                    oneWell = wells[f'{wellCode}']
                    timeSeries = oneWell['lastEmbryoSerie']
                    series = oneWell['series']
                    if timeSeries is None :
                        timeSeries = dishJson["lastSerie"]
                    if timeSeries :
                        oneSeries = series[f'{timeSeries}']
                        jpgName = oneSeries['focus']
                        if jpgName == "cv/embryo_not_found.jpg" :
                            jpgPath = "/static/front/img/loc-emb.png"
                        else :
                            jpgPath = conf['STATIC_NGINX_IMAGE_URL'] + os.path.sep + imagePath + os.path.sep + f'DISH{dishCode}' + os.path.sep + jpgName
                    else :
                        logUtils.info("dish_state.json文件中 lastEmbryoSerie 与 lastSerie 都为空")
                        jpgPath = ""
                else :
                    logUtils.info("采集目录:[%s]未处理完成或皿状态是无效的"%(imagePath))
                    jpgPath = ""
            else :
                logUtils.info(" [%s]文件不存在"%(jsonPath))
                jpgPath = "" 
        else :
            logUtils.info("根据周期ID[%s],皿编号[%s]未查询到对应的数据"%(procedureId,dishCode))
            jpgPath = "" 
    except:
        logUtils.info("获取图片文件出现异常")
        jpgPath = ""
    return jpgPath


def findNewestImageUrl():
    try:
        result = dish_mapper.queryTop3Dish()
        
        dishList = list(map(dict, result))

        if dishList is None :
            return RestResult(200, "最新采集目录下暂无皿信息", 0, "")

        dataList = {}
        data = []
        for dishMap in dishList : 
            imagePath = dishMap["imagePath"]
            jsonPath = conf['EMBRYOAI_IMAGE_ROOT'] + imagePath + os.path.sep + f'DISH{dishMap["dishCode"]}' + os.path.sep + conf['DISH_STATE_FILENAME'] 
            infoMap = dishMap
            infoMap["imagePathShow"] = imagePath[0:4] + "-" + imagePath[4:6] + "-" + imagePath[6:8] + " " + imagePath[8:10] + ":" + imagePath[10:12] + ":" + imagePath[12:14]
            logUtils.info(jsonPath)
            if not os.path.exists(jsonPath) :
                logUtils.info("[%s]文件不存在"%(jsonPath))
                infoMap["wellUrls"] = ""
            else :
                imageUrlList = []
                with open(f'{jsonPath}', 'r') as fn :
                    dishJson = json.loads(fn.read())
                if dishJson['finished'] & dishJson['avail'] == 1 : 
                    hour, minute = serie_to_time(dishJson['lastSerie'])
                    infoMap["times"] = f'{hour:02d}H{minute:02d}M'
                    wells = dishJson['wells']
                    for key in wells:
                        imageObj={}
                        imageObj['wellId'] = key
                        oneWell = wells[f'{key}']
                        series = oneWell['series']
                        timeSeries = oneWell['lastEmbryoSerie']
                        if timeSeries is None :
                            timeSeries = dishJson["lastSerie"]
                        if timeSeries :
                            oneSeries = series[timeSeries]
                            jpgName = oneSeries['focus']
                            if jpgName == "cv/embryo_not_found.jpg" :
                                imageObj['url'] = "/static/front/img/loc-emb.png"
                            else :
                                imageObj['url'] = conf['STATIC_NGINX_IMAGE_URL'] + os.path.sep + imagePath + os.path.sep + f'DISH{dishMap["dishCode"]}' + os.path.sep + jpgName
                        else :
                            logUtils.info("最后一个找到胚胎的时间序列为空")
                            imageObj['url'] = ""
                        imageUrlList.append(imageObj)
                        
                    infoMap["wellUrls"] = imageUrlList
                else :
                    logUtils.info("采集目录:[%s]未处理完成或皿无效"%(imagePath))
                    infoMap["wellUrls"] = ""
            data.append(infoMap)
        if not data:
            dataList["dishInfo"] = ""
        else: 
            dataList["dishInfo"] = data
        return RestResult(200, "查询最新采集目录下的皿信息成功", 1, dataList)
    except Exception as e:
        logUtils.info(traceback.print_exc())
        return RestResult(400, "查询最新采集目录下的皿信息失败", 0, "")


def getBigImagePath(agrs):
    logUtils.info(agrs)
    procedureId = agrs['procedureId']
    dishId = agrs['dishId']
    wellId = agrs['wellId']
    timeSeries = agrs['timeSeries']
    zIndex = agrs['zIndex']
    try:
        dish = dish_mapper.queryById(dishId)
        imagePath,path,dishJson = readDishState(procedureId,dishId)
        url = imagePath + os.path.sep + f'DISH{dish.dishCode}' + os.path.sep 
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
            url = conf['STATIC_NGINX_IMAGE_URL'] + os.path.sep + url + timeSeries + os.path.sep + jpgName
            logUtils.info(url)
            # image = cv2.imread(r'e:\EmbryoAI\EmbryoAI-System\code\python\..\captures\20180422152100\DISH8\7000000\00006.jpg')
            # image = open(jpgPath,'rb').read()
            return RestResult(200, "获取图片路径成功", 1, url)
        else :
            logUtils.info("采集目录[%s]未处理完成或皿状态是无效的"%(imagePath))
            return RestResult(400, "采集目录未处理完成或皿状态是无效的", 0, "")
    except:
        logUtils.info("获取图片路径出现异常")
        return RestResult(400, "获取图片路径失败", 0, "")
    