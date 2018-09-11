from app import db
from entity.ProcedureDish import ProcedureDish
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc

def queryByProcedureIdAndDishId(procedureId,dishId):
    procedureDish = None
    try:
        procedureDish =  db.session.query(ProcedureDish).filter(ProcedureDish.procedureId == procedureId,ProcedureDish.dishId == dishId).one_or_none()
    except Exception as e:
        return procedureDish
    finally:
        db.session.remove()
    return procedureDish

def save(procedureDish):
    try :
        db.session.merge(procedureDish)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('新增周期与培养皿关联数据时发生错误', e.message, e)
    finally:
        db.session.remove()

def queryNewestImagesInfo():
    try:
        count_sql = text("""
            SELECT tpd.image_path imagePath,si.id incubatorId,si.incubator_code incubatorCode
            FROM t_procedure_dish tpd
            LEFT JOIN sys_dish sd ON tpd.dish_id = sd.id
            LEFT JOIN sys_incubator si ON sd.incubator_id = si.id
            ORDER BY tpd.image_path DESC
            LIMIT 0,1
        """)
        print(count_sql)
        # 计算总条数
        count_result = db.session.execute(count_sql)
        data = count_result.fetchone()
        print(data)
        if data is not None:
            imagePath = data[0]
            incubatorId = data[1]
            incubatorCode = data[2]
        return imagePath,incubatorId,incubatorCode
    except Exception as e:
        raise DatabaseError("查询最新采集时间及培养箱信息!",e.message,e)
        return None,None,None
    finally:
        db.session.remove()