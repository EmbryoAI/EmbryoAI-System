from app import db
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc
from entity.Incubator import Incubator


def save(incubator):
    try :
        db.session.merge(incubator)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('新增培养箱数据时发生错误', e.message, e)

def getByIncubatorCode(incubatorCode):
    rs = db.session.query(Incubator).filter(Incubator.incubatorCode == incubatorCode).one_or_none()
    db.session.remove()
    return rs


