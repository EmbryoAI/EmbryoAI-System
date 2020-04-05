from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
    make_response,
    abort,
    session,
)
from flask_restful import reqparse
import logUtils
from app import db
import service.front.statistics_service as statistics_service
from entity.User import User
import time
from app import login_required

statistics_rest_controller = Blueprint("statistics_rest_controller", __name__)
url_prefix = "/api/v1/statistics"


# 时间范围胚胎结局统计
@statistics_rest_controller.route("/embryo/outcome", methods=["GET"])
@login_required
def embryoOutcome():
    logUtils.info("statistics_rest_controller.embryoOutcome-时间范围胚胎结局统计")
    return statistics_service.embryoOutcome(request)


# 时间范围胚胎结局统计
@statistics_rest_controller.route("/milestone/embryos", methods=["GET"])
@login_required
def milestoneEmbryos():
    logUtils.info("statistics_rest_controller.milestoneEmbryos-周期中里程碑点胚胎数统计")
    return statistics_service.milestoneEmbryos()


# 妊娠率统计
@statistics_rest_controller.route("/pregnancy/rate", methods=["GET"])
@login_required
def pregnancyRate():
    logUtils.info("statistics_rest_controller.pregnancyRate-妊娠率统计")
    return statistics_service.pregnancyRate(request)
