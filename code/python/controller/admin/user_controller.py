# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort
from common import logger
from app import db
import service.user_service as user_service
import time
from common import uuid

user_controller = Blueprint('user_controller', __name__)
url_prefix = '/api/v1/user'

#用户修改密码
@user_controller.route('/password', methods=['PUT'])
def password():
    logger().info('进入user_controller.modifyPassword')
    username = request.json.get("username")
    password = request.json.get("password")

    code, msg = user_service.updateUser(username, password)

    return make_response(jsonify(msg), code)

#新增用户
@user_controller.route('/addUser', methods=['POST'])
def addUser():
    if not request.json:
        abort(403)
    if not request.json['username']:
        abort(403)
    id = uuid()
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    mobile = request.json.get('mobile')
    truename = request.json.get('truename')
    title = request.json.get('title')
    is_admin = request.json.get('isAdmin')
    is_private = request.json.get('isPrivate')

    create_time = update_time = last_login_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))    
    
    code, user = user_service.insertUser(id, username, password, email, mobile, truename, title, 
        is_admin, is_private, create_time, update_time, last_login_time)
    return make_response(jsonify(user), code)