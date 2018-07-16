from app import db
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc
from entity.Feedback import Feedback


def insertFeedback(feedback):
    try :
        db.session.merge(feedback)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('插入病历回访数据时发生错误', e.message, e)

def getFeedbackInfo(id):
    sql = text("""
        SELECT t.`procedure_id` as procedureId, t.`biochem_pregnancy` as biochemPregnancy, 
        t.`clinical_pregnancy` as clinicalPregnancy, t.`fetus_count` as fetusCount 
        FROM `t_feedback` t WHERE t.`procedure_id` = :procedureID
        """)
    print(sql)
    return db.session.execute(sql, {'procedureID':id}).fetchone()