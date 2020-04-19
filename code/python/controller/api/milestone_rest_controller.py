# -*- coding: utf8 -*-

from flask import Blueprint, jsonify, render_template, request, make_response, abort
from flask_restful import reqparse
import logUtils
import service.front.milestone_service as milestone_service
from app import login_required

milestone_rest_controller = Blueprint("milestone_rest_controller", __name__)
url_prefix = "/api/v1/milestone"

"""  新增和修改里程碑节点
"""


@milestone_rest_controller.route("/add", methods=["POST"])
@login_required
def addMilestone():
    logUtils.info("milestone_rest_controller.addMilestone-新增和修改里程碑节点")
    code, milestone = milestone_service.insertMilestone(request)
    return make_response(jsonify(milestone), code)


""" #根据胚胎ID、和序列 查询出里程碑相关信息
    @param embryoId: 胚胎ID
    @param timeSeries ： 时间序列
"""


@milestone_rest_controller.route("/<string:embryoId>", methods=["GET"])
@login_required
def getMilestoneByEmbryoId(embryoId):
    logUtils.info(
        "milestone_rest_controller.getMilestoneByEmbryoId-根据胚胎ID、和序列 查询出里程碑相关信息"
    )
    parser = reqparse.RequestParser()
    parser.add_argument("timeSeries", type=str)
    parser.add_argument("procedureId", type=str)
    parser.add_argument("dishId", type=str)
    parser.add_argument("wellId", type=str)
    code, milestone = milestone_service.getMilestoneByEmbryoId(
        embryoId,
        parser.parse_args()["timeSeries"],
        parser.parse_args()["procedureId"],
        parser.parse_args()["dishId"],
        parser.parse_args()["wellId"],
    )
    return make_response(jsonify(milestone), code)


""" 根据胚胎ID 和 当前时间序列 获取上下里程碑节点ID
    @param embryoId: 胚胎ID
    @param milestoneId ： 程牌的节点ID
    @param upOrdown ： up上  down下
    @return 里程碑节点对象
"""


@milestone_rest_controller.route(
    "/node/<string:embryoId>/<string:milestoneTime>/<string:upOrdown>", methods=["GET"]
)
@login_required
def getMilepostNode(embryoId, milestoneTime, upOrdown):
    logUtils.info(
        "milestone_rest_controller.getMilepostNode-根据胚胎ID 和 当前时间序列 获取上下里程碑节点ID"
    )
    code, milestone = milestone_service.getMilepostNode(
        embryoId, milestoneTime, upOrdown
    )
    return make_response(jsonify(milestone), code)


# 根据周期ID和孔ID获取里程碑
@milestone_rest_controller.route("/info", methods=["GET"])
@login_required
def getMilestone():
    logUtils.info("milestone_rest_controller.getMilestone-根据周期ID和孔ID获取里程碑")
    parser = reqparse.RequestParser()
    parser.add_argument("procedureId", type=str)
    parser.add_argument("cellId", type=str)
    return milestone_service.getMilestone(parser.parse_args())
