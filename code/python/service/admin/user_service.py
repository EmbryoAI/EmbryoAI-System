# -*- coding: utf8 -*-

from entity.User import User
from entity.RestResult import RestResult
import dao.admin.user_mapper as user_mapper
from flask import request, jsonify
from common import uuid
import time
import hashlib
import json
from app import login_manager,login_user, logout_user, login_required,current_user

def updatePassword(request):
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        md5 = hashlib.md5()
        md5.update(password.encode(encoding='utf-8'))
        password = md5.hexdigest()
        params = {'username': username, 'password': password}
        user_mapper.updatePassword(params)

        
    except:
        return 400, {'msg': '修改用户密码时发生错误'}
    return 200, {'msg': '修改成功'}

def insertUser(request):

    id = uuid()
    username = request.form.get('username')
    if username == "":
        return 400, '用户名不能为空!'
    password = request.form.get('password')
    if password == "":
        return 400, '密码不能为空!'
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    if email == "" and mobile == "":
        return 400, '手机号码和电子邮箱必须填写一项!!'
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
    return 200, '新增用户成功!'

def findUserById(id):
    return user_mapper.findUserById(id)

def updateUser(request):
    user_id = request.form.get('id')
    if user_id == "":
        return 400, {'获取不到该用户信息!'}
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    if mobile == "" and email == "":
        return 400, {'手机号码和邮箱必须填写一项!'}
    truename = request.form.get('truename')
    if truename == "":
        return 400, {'真实姓名不能为空!'}
    title = request.form.get('title')
    if title == "":
        return 400, {'职称不能为空!'}
    isAdmin = request.form.get('isAdmin')
    if isAdmin == "":
        return 400, {'是否管理员不能为空!'}
    birthday = request.form.get('birthday')
    if birthday == "":
        birthday = None
    usersex = request.form.get('sex')

    updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 

    params = {'id': user_id, 'birthday':birthday, 'email': email, 'mobile': mobile, 'truename': truename, 'title': title, 'is_admin': isAdmin, 'sex': usersex, 'update_time': updateTime}

    try:
        user_mapper.updateUser(params)
    except:
        return 500, '修改用户数据时发生错误!'
    return 200, '修改用户数据成功!'

def findAllUsers(request):
    username = request.args.to_dict().get('username')
    page_number = request.args.to_dict().get('page')
    page_size = request.args.to_dict().get('limit')

    try:
        count = user_mapper.count(username)
        users = list(map(lambda x: x.to_dict(), user_mapper.findAllUsers(page_number, page_size, username)))
    except:
        return 400, '查询用户列表时发生错误!'
    restResult = RestResult(0, "OK", count, users)
    return jsonify(restResult.__dict__)

def deleteUser(id):
    try:
        params = {'id':id}
        user_mapper.deleteUser(params)
    except:
        return 500, '删除用户时发生错误'
    return 200, '删除用户成功'

def updateUserLoginTime(id,lastLoginTime):
    try:
        params = {'id': id, 'lastLoginTime': lastLoginTime}
        user_mapper.updateUserLoginTime(params)
    except:
        return 400, {'msg': '修改用户登录实践时发生错误'}
    return 202, {'msg': '修改成功'}

def userLogin(username,password):
    if username is None or password is None :
        restResult = RestResult(500, "用户名、密码不能为空", 0, None)
        return jsonify(restResult.__dict__)
    md5 = hashlib.md5()
    md5.update(password.encode(encoding='utf-8'))
    password = md5.hexdigest()
    restResult = RestResult(404, "用户不存在或密码错误", 0, None)
    try:
        user = user_mapper.findUserByNameAndPwd(username,password)
        if user is not None :
            login_user(user,True)
            restResult = RestResult(200, "用户登录成功", 1, user.to_dict())
    except:
        restResult = RestResult(404, "用户登录时发生错误", 0, None)
    return jsonify(restResult.__dict__)