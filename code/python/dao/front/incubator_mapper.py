from app import db
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc
from entity.Incubator import Incubator


def save(incubator):
    try:
        db.session.merge(incubator)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError("新增培养箱数据时发生错误", e.message, e)
    finally:
        db.session.remove()


def getByIncubatorCode(incubatorCode):
    try:
        return (
            db.session.query(Incubator)
            .filter(Incubator.incubatorCode == incubatorCode)
            .one_or_none()
        )
    except Exception as e:
        raise DatabaseError("根据培养箱编码获培养箱对象异常！", e.message, e)
        return None
    finally:
        db.session.remove()
