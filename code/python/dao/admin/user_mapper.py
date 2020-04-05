# -*- coding: utf8 -*-

from app import db, app
from entity.User import User
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc
import logUtils


def updatePassword(params):
    try:
        sql = text(
            "update sys_user set password = :password where username = :username"
        )
        logUtils.info(sql)
        db.session.execute(sql, params)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError("修改用户密码时发生错误", e.message, e)
    finally:
        db.session.remove()


def updateUser(params):
    try:
        sql = text(
            "update sys_user set birthday = :birthday, email = :email, is_admin = :is_admin, mobile = :mobile, sex = :sex, title = :title, truename = :truename, update_time = :update_time WHERE id = :id"
        )
        logUtils.info(sql)
        db.session.execute(sql, params)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError("修改用户数据时发生错误", e.message, e)
    finally:
        db.session.remove()


def insertUser(user):
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError("插入用户数据时发生错误", e.message, e)
    finally:
        db.session.remove()


def findUserById(id):
    try:
        return db.session.query(User).filter(User.id == id).one_or_none()
    except Exception as e:
        raise DatabaseError("根据用户ID获取用户对象失败！", e.message, e)
        return None
    finally:
        db.session.remove()


def findAllUsers(page_number, page_size, username):
    try:
        return (
            db.session.query(User)
            .filter(
                User.username.like("%" + username + "%")
                if username is not None
                else "",
                User.delFlag == "0",
            )
            .limit(int(page_size))
            .offset((int(page_number) - 1) * int(page_size))
        )
    except Exception as e:
        raise DatabaseError("查询用户列表失败！", e.message, e)
        return None
    finally:
        db.session.remove()


def count(username):
    try:
        return (
            db.session.query(User)
            .filter(
                User.username.like("%" + username + "%")
                if username is not None
                else "",
                User.delFlag == "0",
            )
            .count()
        )
    except Exception as e:
        raise DatabaseError("查询用户总数失败！", e.message, e)
        return None
    finally:
        db.session.remove()


def deleteUser(params):
    try:
        sql = text("update sys_user set del_flag = 1 where id = :id")
        logUtils.info(sql)
        db.session.execute(sql, params)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError("删除用户数据时发生错误", e.message, e)
    finally:
        db.session.remove()


def findUserByUserName(username):
    try:
        return (
            db.session.query(User)
            .filter(User.username == username, User.delFlag == "0")
            .one_or_none()
        )
    except Exception as e:
        raise DatabaseError("根据用户姓名查询用户对象失败！", e.message, e)
        return None
    finally:
        db.session.remove()


def findUserByNameAndPwd(username, password):
    try:
        return (
            db.session.query(User)
            .filter(
                User.username == username,
                User.password == password,
                User.delFlag == "0",
            )
            .one_or_none()
        )
    except Exception as e:
        raise DatabaseError("根据帐号密码查询用户失败！", e.message, e)
        return None
    finally:
        db.session.remove()


def updateUserLoginTime(params):
    try:
        sql = text(
            "update sys_user set last_login_time = :lastLoginTime where id = :id"
        )
        logUtils.info(sql)
        logUtils.info(params["lastLoginTime"])
        db.session.execute(sql, params)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError("修改用户登录时间发生错误", e.message, e)
    finally:
        db.session.remove()
