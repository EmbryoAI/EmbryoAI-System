from flask import Blueprint, render_template
from flask_restful import reqparse
import logUtils
from app import login_required
import service.front.embryo_service as embryo_service

""" 胚胎视图 """

embryo_controller = Blueprint("embryo_controller", __name__)
url_prefix = "/front/embryo"


@embryo_controller.route("/", methods=["GET"])
@login_required
def main():
    logUtils.info("embryo_controller.main-跳转到胚胎视图页面")
    parser = reqparse.RequestParser()
    parser.add_argument("procedureId", type=str)
    parser.add_argument("dishId", type=str)
    parser.add_argument("embryoId", type=str)
    parser.add_argument("cellCode", type=str)
    parser.add_argument("dishCode", type=str)

    agrs = parser.parse_args()
    procedureId = agrs["procedureId"]
    dishId = agrs["dishId"]
    embryoId = agrs["embryoId"]
    cellCode = agrs["cellCode"]
    dishCode = agrs["dishCode"]
    return render_template(
        "front/embryo/embryo.html",
        procedure_id=procedureId,
        dish_id=dishId,
        embryo_id=embryoId,
        cell_code=cellCode,
        dishCode=dishCode,
    )


@embryo_controller.route("/toEmbryo", methods=["GET"])
@login_required
def toEmbryo():
    logUtils.info("embryo_controller.toEmbryo-跳转到胚胎视图页面")
    parser = reqparse.RequestParser()
    parser.add_argument("imagePath", type=str)
    parser.add_argument("dishId", type=str)
    parser.add_argument("wellCode", type=str)
    parser.add_argument("dishCode", type=str)

    agrs = parser.parse_args()
    wellCode = agrs["wellCode"]
    dishCode = agrs["dishCode"]

    procedureId, dishId, embryoId = embryo_service.findEmbroyoInfo(agrs)
    return render_template(
        "front/embryo/embryo.html",
        procedure_id=procedureId,
        dish_id=dishId,
        embryo_id=embryoId,
        cell_code=wellCode,
        dishCode=dishCode,
    )
