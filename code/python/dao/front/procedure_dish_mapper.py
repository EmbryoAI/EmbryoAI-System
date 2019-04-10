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
            SELECT tpd.image_path imagePath
            FROM t_procedure_dish tpd
            LEFT JOIN t_procedure tp ON tpd.procedure_id = tp.id
            WHERE tp.del_flag = 0
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
        return imagePath
    except Exception as e:
        raise DatabaseError("查询最新采集时间及培养箱信息!",e.message,e)
        return None
    finally:
        db.session.remove()

def queryByImagePathAndDishId(imagePath,dishId):
    procedureDish = None
    try:
        procedureDish =  db.session.query(ProcedureDish).filter(ProcedureDish.imagePath == imagePath,ProcedureDish.dishId == dishId).one_or_none()
    except Exception as e:
        return procedureDish
    finally:
        db.session.remove()
    return procedureDish

def queryEmbryoId(imagePath,dishId,cellCode):
    try:
        sql = text("""
            SELECT tpd.procedure_id procedureId,te.id embryoId
            FROM t_procedure_dish tpd
            LEFT JOIN t_embryo te ON tpd.procedure_id = te.procedure_id
            LEFT JOIN sys_cell sc ON te.cell_id = sc.id AND tpd.dish_id = sc.dish_id
            WHERE tpd.image_path = :imagePath AND sc.dish_id = :dishId AND sc.cell_code = :cellCode
        """)
        print(sql)
        # 计算总条数
        count_result = db.session.execute(sql,{'imagePath':imagePath,'dishId':dishId,'cellCode':cellCode})
        data = count_result.fetchone()
        print(data)
        if data is not None:
            procedureId = data[0]
            embryoId = data[1]
        return procedureId,embryoId
    except Exception as e:
        raise DatabaseError("查询最新采集时间及培养箱信息!",e.message,e)
        return None,None
    finally:
        db.session.remove()

def queryAllCatalog():
    try:
        sql = text("""
            SELECT tpd.`image_path` AS relation_catalog FROM `t_procedure_dish` tpd 
        """)
        print(sql)
        # 计算总条数
        data = db.session.execute(sql).fetchall()
        return data
    except Exception as e:
        raise DatabaseError("查询所以关联病例采集目录信息!",e.message,e)
        return None
    finally:
        db.session.remove()