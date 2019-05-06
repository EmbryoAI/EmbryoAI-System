from app import db
from entity.Procedure import Procedure
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc
from entity.Patient import Patient
import logUtils


def update(id, mobile, email):
    try:
        sql = text("UPDATE `t_patient` SET mobile = :mobile, email = :email WHERE id = :id")
        logUtils.info(sql)
        db.session.execute(sql,{'id':id, 'mobile':mobile, 'email':email})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError("修改patient信息时发生错误",e.message,e)
    finally:
        db.session.remove()
    
def queryPatientNameList(sqlCondition,filters):
    try:
        sql = text("""
           SELECT patient_name AS 'value',patient_name AS label FROM  t_patient
        """+sqlCondition)
    
        # 执行sql得出结果
        result = db.session.execute(sql,filters) 
        sql_result = result.fetchall()
        return sql_result
    except Exception as e:
        raise DatabaseError("queryPatientNameList异常",e.message,e)
        return None
    finally:
        db.session.remove()
        
def save(patient):
    try :
        db.session.add(patient)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('新增患者数据时发生错误', e.message, e)
    finally:
        db.session.remove()

def getByPatientId(id):
    try :
        return db.session.query(Patient).filter(Patient.id == id).one_or_none()
    except Exception as e:
        raise DatabaseError("getByPatientId异常",e.message,e)
        return None
    finally:
        db.session.remove()