# -*- coding: utf8 -*-

from entity.User import User
import dao.user_mapper as user_mapper

def updateUser(username, password):
    try:
        params = {'username': username, 'password': password}
        user_mapper.updateUser(params)
    except:
        return 400, {'msg': '修改用户密码时发生错误'}
    return 202, {'msg': '修改成功'}