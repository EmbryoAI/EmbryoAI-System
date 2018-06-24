# -*- coding: utf8 -*-

from app import db
from entity.Incubator import Incubator
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc

def insertIncubator(incubator):
    try :
        db.session.add(incubator)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('插入培养箱数据时发生错误', e.message, e)

def findIncubatorById(id):
    return db.session.query(Incubator).filter(Incubator.id == id).one_or_none()

def findIncubatorByCode(incubatorCode):
    return db.session.query(Incubator).filter(Incubator.incubatorCode == incubatorCode).one_or_none()


def queryIncubatorList(page,limit,filters):
    pagination = Incubator.query.filter_by(**filters).order_by(Incubator.createTime.desc()).paginate(page,per_page=limit,error_out=False)
    return pagination


def updateIncubator(params):
    try :
        sql = text('update sys_incubator set incubator_code=:incubatorCode,incubator_brand=:incubatorBrand, incubator_type=:incubatorType'
        ', incubator_description=:incubatorDescription '
        ', update_time=:updateTime '
            'where id=:id')
        print(sql)
        db.session.execute(sql, params)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('编辑培养箱异常', e.message, e)
    
def deleteIncubator(params):
    try :
        sql = text('update sys_incubator set del_flag=:delFlag '
            'where id=:id')
        print(sql)
        db.session.execute(sql, params)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('删除培养箱异常', e.message, e)