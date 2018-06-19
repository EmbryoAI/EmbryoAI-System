# -*- coding: utf8 -*-

from entity.User import User
import dao.admin.user_mapper as user_mapper
from flask import request
from common import uuid
import time

def updateUser(username, password):
    try:
        params = {'username': username, 'password': password}
        user_mapper.updateUser(params)
    except:
        return 400, {'msg': '修改用户密码时发生错误'}
    return 202, {'msg': '修改成功'}

def insertUser(request):

    id = uuid()
    username = request.form.get('username')
    if username == "":
        return 400, '用户名不能为空!'
    password = request.form.get('password')
    if password == "":
        return 400, '密码不能为空!'
    email = request.form.get('email')
    if email == "":
        return 400, '电子邮箱不能为空!'
    mobile = request.form.get('mobile')
    if mobile == "":
        return 400, '手机号码不能为空!'
    truename = request.form.get('truename')
    if truename == "":
        return 400, '真实姓名不能为空!'
    title = request.form.get('title')
    if title == "":
        return 400, '职称不能为空!'
    is_admin = request.form.get('isAdmin')
    if is_admin == "":
        return 400, '是否管理员不能为空!'
    is_private = request.form.get('isPrivate')
    if is_private == "":
        return 400, '病历权限不能为空!'

    create_time = update_time = last_login_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 

    user = user_mapper.findUserByUserName(username)
    if user:
        return 401, '用户名已存在!!'

    user = User(id=id, username=username, password=password, email=email, mobile=mobile, truename=truename, 
        title=title, isAdmin=is_admin, isPrivate=is_private, createTime=create_time, updateTime=update_time, 
        lastLoginTime=last_login_time)
    try:
        user_mapper.insertUser(user)
    except:
        return 400, '新增用户时发生错误!'
    return 200, user.to_dict()

def findUserById(id):
    return user_mapper.findUserById(id)

def findAllUsers():
    return user_mapper.findAllUsers()

def deleteUser(user):
    try:
        user_mapper.deleteUser(user)
    except:
        return 400, {'msg': '删除用户时发生错误'}
    return 204, None

def updateUserLoginTime(id,lastLoginTime):
    try:
        params = {'id': id, 'lastLoginTime': lastLoginTime}
        user_mapper.updateUserLoginTime(params)
    except:
        return 400, {'msg': '修改用户登录实践时发生错误'}
    return 202, {'msg': '修改成功'}

def findUserByNameAndPwd(username,password):
    return user_mapper.findUserByNameAndPwd(username,password)