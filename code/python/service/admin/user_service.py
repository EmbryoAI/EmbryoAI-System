# -*- coding: utf8 -*-

from entity.User import User
import dao.admin.user_mapper as user_mapper

def updateUser(username, password):
    try:
        params = {'username': username, 'password': password}
        user_mapper.updateUser(params)
    except:
        return 400, {'msg': '修改用户密码时发生错误'}
    return 202, {'msg': '修改成功'}

def insertUser(id, username, password, email, mobile, truename, title, is_admin, is_private, create_time, 
                update_time, last_login_time):
    user = User(id=id, username=username, password=password, email=email, mobile=mobile, truename=truename, 
        title=title, isAdmin=is_admin, isPrivate=is_private, createTime=create_time, updateTime=update_time, 
        lastLoginTime=last_login_time)
    try:
        user_mapper.insertUser(user)
    except:
        return 400, {'msg': '新增用户时发生错误'}
    return 201, user.to_dict()

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