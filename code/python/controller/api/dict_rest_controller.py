# -*- coding: utf8 -*-

from flask import Blueprint
import logUtils
import service.front.dict_service as dict_service

dict_rest_controller = Blueprint("dict_rest_controller", __name__)
url_prefix = "/api/v1/dict"


@dict_rest_controller.route("/list/<string:dictClass>", methods=["GET"])
def queryDictListByClass(dictClass):
    """ 根据字典类别获取对应的字典列表
        @param dictClass: 字典类别
    """
    logUtils.info("进入dict_rest_controller.queryDictListByClass-查询字典列表")
    return dict_service.queryDictListByClass(dictClass)


@dict_rest_controller.route("/lists/<string:dictClass>", methods=["GET"])
def queryDictListByClassS(dictClass):
    """ 根据逗号隔开多个字典类别获取列表，减少ajax请求
        @param dictClass: 多个字典类别 使用,隔开
    """
    logUtils.info("进入dict_rest_controller.queryDictListByClassS-查询字典列表")
    return dict_service.queryDictListByClassS(dictClass)


@dict_rest_controller.route("/list/parent/<string:dictParentId>", methods=["GET"])
def queryDictListByDictParentId(dictParentId):
    """ 根据父级字典ID获取子集字典列表
        @param dictParentId: 父级字典ID
    """
    logUtils.info("进入dict_rest_controller.queryDictListByDictParentId-根据父级字典ID获取子集字典列表")
    return dict_service.queryDictListByDictParentId(dictParentId)
