# -*- coding: utf8 -*-
from entity.RestResult import RestResult
import service.front.image_service as image_service
import dao.front.embryo_mapper as embryo_mapper
from flask import request, jsonify
from common import uuid, logger
from app import conf
import json, os
from common import getdefault


def queryClearImageUrl(agrs):
    procedureId = agrs["procedureId"]
    dishId = agrs["dishId"]
    wellId = agrs["wellId"]
    zData = {}
    nginxImageUrl = getdefault(conf, "STATIC_NGINX_IMAGE_URL", "http://localhost:80")
    try:
        # 获取JSON文件
        path, dishJson = image_service.getImagePath(procedureId, dishId)
        clearImageUrlList = []

        if dishJson["avail"] == 1:
            wells = dishJson["wells"]
            oneWell = wells[f"{wellId}"]
            series = oneWell["series"]
            for key in series:
                imageObj = {}
                imageObj["clearImageUrl"] = (
                    nginxImageUrl
                    + os.path.sep
                    + path
                    + key
                    + os.path.sep
                    + series[key]["sharp"]
                )
                #                 thumbnailUrl = nginxImageUrl+os.path.sep+path + series[key]['focus']
                #                 imageObj['thumbnailUrl'] = thumbnailUrl
                imageObj["timeSeries"] = key
                clearImageUrlList.append(imageObj)
        if not clearImageUrlList:
            return 200, None
        else:
            return 200, clearImageUrlList
    except:
        return 400, "获取孔的时间序列对应最清晰的URL异常!"


def fenye(datas, pagenum, pagesize):
    if datas and isinstance(pagenum, int) and isinstance(pagesize, int):
        return datas[((pagenum - 1) * pagesize) : ((pagenum - 1) * pagesize) + pagesize]


def queryThumbnailImageUrl(agrs):
    procedureId = agrs["procedureId"]
    dishId = agrs["dishId"]
    wellId = agrs["wellId"]
    zData = {}
    nginxImageUrl = getdefault(conf, "STATIC_NGINX_IMAGE_URL", "http://localhost:80")
    try:
        # 获取JSON文件
        path, dishJson = image_service.getImagePath(procedureId, dishId)
        thumbnailUrlList = []
        result = {}
        embryoId = None
        if dishJson["avail"] == 1:
            wells = dishJson["wells"]
            oneWell = wells[f"{wellId}"]
            series = oneWell["series"]
            for key in series:
                imageObj = {}
                if series[key]["focus"] == "cv/embryo_not_found.jpg":
                    thumbnailUrl = "/static/front/img/loc-emb.png"
                else:
                    thumbnailUrl = (
                        nginxImageUrl + os.path.sep + path + series[key]["focus"]
                    )
                imageObj["thumbnailUrl"] = thumbnailUrl
                imageObj["timeSeries"] = key
                thumbnailUrlList.append(imageObj)

            """根据动态条件获取胚胎ID、孔ID、胚胎结局、里程碑等相关信息  """
            if embryoId == None:
                sql = " t.procedure_id = :procedureId AND sc.dish_id = :dishId AND sc.cell_code = :cellCode "
                filters = {
                    "procedureId": procedureId,
                    "dishId": dishId,
                    "cellCode": wellId,
                }
                embryo = embryo_mapper.getEmbryoByCondition(sql, filters)
            result["thumbnailUrlList"] = thumbnailUrlList
            result["embryo"] = dict(embryo)
        if not result:
            return 200, None
        else:
            return 200, result
    except:
        return 200, None
