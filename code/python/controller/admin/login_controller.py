# -*- coding: utf8 -*-

from flask import Blueprint, render_template
import logUtils
from app import logout_user, login_required

login_controller = Blueprint("login_controller", __name__)
url_prefix = "/login"


@login_controller.route("/", methods=["GET"])
def index():
    logUtils.info("login_controller.index-跳转到前台管理的login页面")
    return render_template("login.html")


@login_controller.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    logUtils.info("login_controller.logout-退出并跳转到前台管理的login页面")
    return render_template("login.html", msg="You have been logged out.")
    ###重定向到首页


@login_controller.route("/main", methods=["GET", "POST"])
@login_required
def toAdmin():
    logUtils.info("login_controller.toAdmin-跳转到后台管理的main页面")
    return render_template("admin/main.html")
    ###重定向到首页


@login_controller.route("/front", methods=["GET", "POST"])
@login_required
def toFront():
    logUtils.info("login_controller.toFront-跳转到前台的home页面")
    return render_template("front/home.html")
