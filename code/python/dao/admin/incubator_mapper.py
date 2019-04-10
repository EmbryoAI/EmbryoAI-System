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
    finally:
        db.session.remove()

def findIncubatorById(id):
    try:
        return db.session.query(Incubator).filter(Incubator.id == id).one_or_none()
    except Exception as e:
        raise DatabaseError('根据培养箱ID获取培养箱失败！', e.message, e)
        return None
    finally:
        db.session.remove()

def findIncubatorByCode(incubatorCode):
    try:
        return db.session.query(Incubator).filter(Incubator.incubatorCode == incubatorCode).one_or_none()
    except Exception as e:
        raise DatabaseError('根据培养箱并编码获取培养箱失败！', e.message, e)
        return None
    finally:
        db.session.remove()


def queryIncubatorList(page,limit,filters):
    try:
        pagination = Incubator.query.filter_by(**filters).order_by(Incubator.createTime.desc()).paginate(page,per_page=limit,error_out=False)
        return pagination
    except Exception as e:
        raise DatabaseError('根据培养箱并编码获取培养箱失败！', e.message, e)
        return None
    finally:
        db.session.remove()

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
    finally:
        db.session.remove()
    
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
    finally:
        db.session.remove()
        
#根据皿ID获取培养箱编码
def getIncubatorCodeByDishId(dishId):
    try:
        sql = text("""
            SELECT b.incubator_code as incubatorCode FROM sys_dish di
            LEFT JOIN sys_incubator b 
            ON di.incubator_id=b.id
            WHERE di.id=:dishId
            """)
        count_result = db.session.execute(sql,{"dishId":dishId})
        return count_result.fetchone()[0]
    except Exception as e:
        print_exc()
        raise DatabaseError("根据皿ID获取培养箱编码异常!",e.message,e)
        return None
    finally:
        db.session.remove()