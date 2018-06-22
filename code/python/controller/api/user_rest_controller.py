# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
from common import logger
from app import db
import service.admin.user_service as user_service
from entity.User import User
import time


user_rest_controller = Blueprint('user_rest_controller', __name__)
url_prefix = '/api/v1/user'


#用户修改密码
@user_rest_controller.route('/password', methods=['PUT'])
def password():
    logger().info('进入user_controller.modifyPassword')
    username = request.json.get("username")
    password = request.json.get("password")

    code, msg = user_service.updateUser(username, password)

    return make_response(jsonify(msg), code)

#新增用户
@user_rest_controller.route('', methods=['POST'])
def addUser():   
    code, user = user_service.insertUser(request)
    return make_response(jsonify(user), code)

#根据用户id查询用户信息
@user_rest_controller.route('/<string:id>', methods=['GET'])
def getUserById(id):
    user = user_service.findUserById(id)
    if not user:
        return make_response(jsonify("当前用户不存在"), 404)
    return jsonify(user.to_dict())

#查询所有用户
@user_rest_controller.route('', methods=['GET'])
def getAllUsers():
    return user_service.findAllUsers()

#根据id删除用户
@user_rest_controller.route('/<string:id>', methods=['DELETE'])
def deleteUser(id):
    user = user_service.findUserById(id)
    if not user:
        abort(404)
    code, msg = user_service.deleteUser(user)
    return make_response(jsonify(msg), code)

'''根据用户名、密码登录'''
parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)
parser.add_argument('isLoginAdmin', type=str)
@user_rest_controller.route('/login',methods=['POST'])
def login():
    args = parser.parse_args()
    if not args or args is None :
        return render_template('/login.html',msg="参数不能为空")
    username = args["username"]
    password = args["password"]
    isLoginAdmin = args["isLoginAdmin"]
    if username is None or password is None :
        logger().info("")
        return render_template('/login.html',msg="用户名、密码不能为空")
    user = user_service.findUserByNameAndPwd(username,password)
    if not user :
        return render_template('/login.html',msg="此用户不存在")
    lastLoginTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    user_service.updateUserLoginTime(user.id,lastLoginTime)
    session["user"] = user.to_dict()
    if user.isAdmin != 0 :
        if isLoginAdmin == "1":
            return render_template('/admin/main.html',user=user)
        else:
            return render_template('/home.html',user=user)
    else:
        return render_template('/home.html',user=user)
    

