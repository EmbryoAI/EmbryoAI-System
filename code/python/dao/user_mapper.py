# -*- coding: utf8 -*-

from app import db
from entity.User import User
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc

def updateUser(params):
    try :
        sql = text('update sys_user set password = :password where username = :username')
        print(sql)
        db.session.execute(sql, params)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('插入用户数据时发生错误', e.message, e)

def insertUser(user):
    try :
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('插入用户数据时发生错误', e.message, e)

def findUserById(id):
    return db.session.query(User).filter(User.id == id).one_or_none()

def findAllUsers():
    return db.session.query(User).all()

def deleteUser(user):
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('删除用户数据时发生错误', e.message, e)