# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
import service.admin.user_service as user_service
from entity.User import User
import time
import hashlib
from common import logger
from app import login_manager,login_user, logout_user, login_required 

login_controller = Blueprint('login_controller', __name__)
url_prefix = '/api/v1/login'

#根据用户id查询用户信息
@login_controller.route('/<string:id>', methods=['GET'])
@login_required
def getUserById(id):
    user = user_service.findUserById(id)
    if not user:
        return make_response(jsonify("当前用户不存在"), 404)
    return jsonify(user.to_dict())

'''根据用户名、密码登录'''
parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)
parser.add_argument('isLoginAdmin', type=str)
@login_controller.route('/login',methods=['POST','GET'])
def login():
    args = parser.parse_args()
    if not args or args is None :
        return render_template('/login.html',msg="参数不能为空")
    username = args["username"]
    password = args["password"]
    isLoginAdmin = args["isLoginAdmin"]
    if username is None or password is None :
        logger().info("用户名、密码不能为空")
        return render_template('/login.html',msg="用户名、密码不能为空")
    md5 = hashlib.md5()
    md5.update(password.encode(encoding='utf-8'))
    password = md5.hexdigest()
    user = user_service.findUserByNameAndPwd(username,password)
    if not user :
        logger().info("此用户不存在或用户名、密码错误")
        return render_template('/login.html',msg="此用户不存在或用户名、密码错误",username=username,password=password)
    #session["user"] = user.to_dict()
    login_user(user,True)
    if user.isAdmin != 0 :
        if isLoginAdmin == "1":
            logger().info("管理员登录后台主页")
            return render_template('/admin/main.html',username=username)
        else:
            logger().info("管理员登录前台主页")
            return render_template('/home.html',username=username)
    else:
        logger().info("非管理员登录前台主页")
        return render_template('/home.html',username=username)

@login_controller.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    ###登出用户，这个视图函数调用logout_user()函数，删除并重设用户会话。
    #flash('')
    ###显示flash消息
    return render_template('login.html',msg="You have been logged out.")
    ###重定向到首页