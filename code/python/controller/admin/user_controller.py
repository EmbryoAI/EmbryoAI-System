# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response
from common import logger
from app import db
import service.user_service as user_service

user_controller = Blueprint('user_controller', __name__)
url_prefix = '/api/v1/user'

@user_controller.route('/password', methods=['PUT'])
def password():
    logger().info('进入user_controller.modifyPassword')
    username = request.json.get("username")
    password = request.json.get("password")
    print("username:", username)
    print("password:", password)

    code, msg = user_service.updateUser(username, password)

    return make_response(jsonify(msg), code)
