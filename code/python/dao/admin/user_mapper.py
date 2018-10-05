# -*- coding: utf8 -*-

from app import db, app
from entity.User import User
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc

def updatePassword(params):
    try :
        sql = text('update sys_user set password = :password where username = :username')
        print(sql)
        db.session.execute(sql, params)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('修改用户密码时发生错误', e.message, e)
    finally:
        db.session.remove()

def updateUser(params):
    try :
        sql = text('update sys_user set birthday = :birthday, email = :email, is_admin = :is_admin, mobile = :mobile, sex = :sex, title = :title, truename = :truename, update_time = :update_time WHERE id = :id')
        print(sql)
        db.session.execute(sql, params)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('修改用户数据时发生错误', e.message, e)
    finally:
        db.session.remove()

def insertUser(user):
    try :
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('插入用户数据时发生错误', e.message, e)
    finally:
        db.session.remove()

def findUserById(id):
    # return db.session.query(User).filter(User.id == id).one_or_none()
    rs = db.session.query(User).filter(User.id == id).one_or_none()
    db.session.remove()
    return rs

def findAllUsers(page_number, page_size, username):
    return db.session.query(User).filter(User.username.like("%"+username+"%") if username is not None else "",User.delFlag=="0").limit(int(page_size)).offset((int(page_number)-1)*int(page_size))

def count(username):
    return db.session.query(User).filter(User.username.like("%"+username+"%") if username is not None else "",User.delFlag=="0").count()

def deleteUser(params):
    try:
        sql = text('update sys_user set del_flag = 1 where id = :id')
        print(sql)
        db.session.execute(sql, params)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('删除用户数据时发生错误', e.message, e)
    finally:
        db.session.remove()


def findUserByUserName(username):
    return db.session.query(User).filter(User.username == username, User.delFlag == '0').one_or_none()


def findUserByNameAndPwd(username,password):
    return db.session.query(User).filter(User.username == username,User.password == password,User.delFlag == '0').one_or_none()

def updateUserLoginTime(params):
    try:
        sql = text("update sys_user set last_login_time = :lastLoginTime where id = :id")
        print(sql)
        print(params['lastLoginTime'])
        db.session.execute(sql,params)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError("修改用户登录时间发生错误",e.message,e)
    finally:
        db.session.remove()
