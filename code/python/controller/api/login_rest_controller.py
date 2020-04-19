# -*- coding: utf8 -*-

from flask import Blueprint, jsonify, request, make_response
from flask_restful import reqparse
import service.admin.user_service as user_service
import logUtils

login_rest_controller = Blueprint("login_rest_controller", __name__)
url_prefix = "/api/v1/login"

# 根据用户名、密码登录
@login_rest_controller.route("/nameAndPwd", methods=["POST"])
def login():
    logUtils.info("login_rest_controller.login-根据用户名、密码登录")
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str)
    parser.add_argument("password", type=str)
    args = parser.parse_args()
    username = args["username"]
    password = args["password"]
    return user_service.userLogin(username, password)
