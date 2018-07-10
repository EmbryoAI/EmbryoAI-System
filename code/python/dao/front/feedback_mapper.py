from app import db
from entity.Procedure import Procedure
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc
from entity.Feedback import Feedback


def insertFeedback(feedback):
    try :
        db.session.add(feedback)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('插入病历回访数据时发生错误', e.message, e)
