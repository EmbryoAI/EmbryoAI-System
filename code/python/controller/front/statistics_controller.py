from flask import Blueprint, render_template
from app import login_required
import logUtils

""" 统计模块 """

statistics_controller = Blueprint("statistics_controller", __name__)
url_prefix = "/front/statistics"


@statistics_controller.route("/", methods=["GET"])
@login_required
def main():
    logUtils.info("statistics_controller.main-跳转到统计页面")
    return render_template("front/statistics/statistics.html", htmlType="statistics")
