# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
import logUtils
from app import db
import service.admin.user_service as user_service
from entity.User import User
import time
from app import login_required,login_user,logout_user


user_rest_controller = Blueprint('user_rest_controller', __name__)
url_prefix = '/api/v1/user'


#用户修改密码
@user_rest_controller.route('/password', methods=['POST'])
@login_required
def password():
    logUtils.info('user_rest_controller.password-用户修改密码')
    code, msg = user_service.updatePassword(request)
    return make_response(jsonify(msg), code)


#新增用户
@user_rest_controller.route('', methods=['POST'])
@login_required
def addUser():
    logUtils.info('user_rest_controller.addUser-新增用户')
    code, user = user_service.insertUser(request)
    return make_response(jsonify(user), code)

#根据用户id查询用户信息
@user_rest_controller.route('/<string:id>', methods=['GET'])
@login_required
def getUserById(id):
    logUtils.info('user_rest_controller.getUserById-根据用户id查询用户信息')
    user = user_service.findUserById(id)
    if not user:
        return make_response(jsonify("当前用户不存在"), 404)
    return jsonify(user.to_dict())

#查询所有用户
@user_rest_controller.route('', methods=['GET'])
@login_required
def getAllUsers():
    logUtils.info('user_rest_controller.getAllUsers-查询所有用户')
    return user_service.findAllUsers(request)

#修改用户数据
@user_rest_controller.route('/userInfo', methods=['POST'])
@login_required
def updateUser():
    logUtils.info('user_rest_controller.updateUser-修改用户数据')
    code, msg = user_service.updateUser(request)
    return make_response(msg, code)
    
#根据id删除用户
@user_rest_controller.route('/<string:id>', methods=['DELETE'])
@login_required
def deleteUser(id):
    logUtils.info('user_rest_controller.deleteUser-根据id删除用户')
    code, msg = user_service.deleteUser(id)
    return make_response(jsonify(msg), code)

