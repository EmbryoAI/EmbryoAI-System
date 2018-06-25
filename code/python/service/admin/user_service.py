# -*- coding: utf8 -*-

from entity.User import User
from entity.RestResult import RestResult
import dao.admin.user_mapper as user_mapper
from flask import request, jsonify
from common import uuid
import time
import hashlib
import json

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
    birthday = request.form.get('birthday')
    sex = request.form.get('sex')

    create_time = update_time = last_login_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 

    user = user_mapper.findUserByUserName(username)
    if user:
        return 401, '用户名已存在!'

    md5 = hashlib.md5()
    md5.update(password.encode(encoding='utf-8'))
    password = md5.hexdigest()

    user = User(id=id, username=username, password=password, email=email, mobile=mobile, truename=truename, 
        title=title, isAdmin=is_admin, isPrivate=is_private, sex=sex, birthday=birthday, createTime=create_time, 
        updateTime=update_time, 
        lastLoginTime=last_login_time)
    try:
        user_mapper.insertUser(user)
    except:
        return 400, '新增用户时发生错误!'
    return 200, user.to_dict()

def findUserById(id):
    return user_mapper.findUserById(id)

def findAllUsers():
    try:
        users = list(map(lambda x: x.to_dict(), user_mapper.findAllUsers()))
    except:
        return 400, '查询用户列表时发生错误!'
    restResult = RestResult(0, "OK", len(users), users)
    return jsonify(restResult.__dict__)

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