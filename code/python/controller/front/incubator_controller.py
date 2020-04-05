from flask import Blueprint, render_template
from flask_restful import reqparse
import logUtils
from app import login_required

""" 培养箱视图 """
incubator_controller = Blueprint("incubator_controller", __name__)
url_prefix = "/front/incubator"


@incubator_controller.route("/", methods=["GET"])
@login_required
def incubator():
    logUtils.info("incubator_controller.incubator-跳转到培养箱视图页面")
    parser = reqparse.RequestParser()
    parser.add_argument("incubatorId", type=str)
    parser.add_argument("procedureId", type=str)

    agrs = parser.parse_args()
    incubatorId = agrs["incubatorId"]
    procedureId = agrs["procedureId"]

    if incubatorId is None:
        incubatorId = ""
    if procedureId is None:
        procedureId = ""

    return render_template(
        "front/incubator/incubator.html",
        incubatorId=incubatorId,
        procedureId=procedureId,
    )
