from app import db
from sqlalchemy import text
from entity.Embryo import Embryo

def queryEmbryoList(procedureID):
    try:
        sql = text("""
            SELECT t.`id`, t.`embryo_index`, sc.`cell_code`, sd.`dish_code`, si.`incubator_code`, sc.`dish_id` 
            FROM `t_embryo` t 
            LEFT JOIN `sys_cell` sc 
            ON t.`cell_id` = sc.`id` 
            LEFT JOIN `sys_dish` sd 
            ON sc.`dish_id` = sd.`id` 
            LEFT JOIN `sys_incubator` si 
            ON sd.`incubator_id` = si.`id` 
            WHERE t.`procedure_id` = :procedureID
            """)
        print(sql)
        return db.session.execute(sql, {'procedureID':procedureID}).fetchall()
    except Exception as e:
        raise DatabaseError("根据周期ID获取下面的胚胎列表异常",e.message,e)
        return None
    finally:
        db.session.remove()

def signEmbryo(id, embryoFateId):
    try:
        sql = text("UPDATE `t_embryo` SET embryo_fate_id = :embryoFateId WHERE id = :id")
        print(sql)
        db.session.execute(sql,{'id':id, 'embryoFateId':embryoFateId})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError("标记胚胎结局时发生错误",e.message,e)
    finally:
        db.session.remove()
        
def getEmbryoById(id):
    try:
        return db.session.query(Embryo).filter(Embryo.id == id).one_or_none()
    except Exception as e:
        raise DatabaseError("根据主键ID获取胚胎异常",e.message,e)
        return None
    finally:
        db.session.remove()
 
def getEmbryoById(id):
    try:
        sql = text("""
            SELECT
              a.id           AS id,
              embryo_index   AS embryoIndex,
              procedure_id   AS procedureId,
              cell_id        AS cellId,
              embryo_score   AS embryoScore,
              embryo_fate_id AS embryoFateId,
              d.dict_spare   AS dictSpare
            FROM t_embryo a
              LEFT JOIN sys_dict d
                ON a.embryo_fate_id = d.dict_key
                  AND d.dict_class = 'embryo_fate_type'
            where a.id=:id
            """)
        print(sql)
        return db.session.execute(sql,{'id':id}).fetchone()
    except Exception as e:
        raise DatabaseError("根据主键ID获取胚胎异常ID异常",e.message,e)
        return None
    finally:
        db.session.remove()

"""根据胚胎ID 获取患者姓名  年龄等数据"""
def getPatientByEmbryoId(id):
     try:
         sql = text("""
                 SELECT
                   e.embryo_index AS embryo_index,
                   pa.patient_name   AS patient_name,
                   pr.patient_age    AS patient_age,
                   CONCAT('D',DATEDIFF(IF(pr.cap_end_time,pr.cap_end_time,NOW()),pr.insemi_time)) AS zzjd
                 FROM t_embryo e
                   LEFT JOIN t_procedure pr
                     ON e.procedure_id = pr.id
                   LEFT JOIN t_patient pa
                     ON pr.patient_id = pa.id
                 where e.id=:id
                 GROUP BY pr.id
             """)
         print(sql)
         return db.session.execute(sql,{'id':id}).fetchone()
     except Exception as e:
         raise DatabaseError("根据主键ID获取胚胎异常ID异常",e.message,e)
         return None
     finally:
         db.session.remove()

"""
    根据皿ID和孔序号获取孔ID  ，再根据周期ID和孔ID 获取 胚胎ID
    @param sqlCondition
    @param filters
"""
def getEmbryoByCondition(sqlCondition,filters):
    try :
        sql = text("""
            SELECT
              t.id           AS id,
              t.cell_id         cellId,
              d.dict_spare AS ptjj,
              GROUP_CONCAT(d1.dict_value,"#",m.milestone_time ORDER BY m.milestone_time) lcb
            FROM t_embryo t
              LEFT JOIN sys_cell sc
                ON t.cell_id = sc.id
              LEFT JOIN t_milestone m
                ON t.id = m.embryo_id
              LEFT JOIN sys_dict d
                ON t.embryo_fate_id = d.dict_key AND d.dict_class = 'embryo_fate_type'
              LEFT JOIN sys_dict d1
                ON m.milestone_id = d1.dict_key AND d1.dict_class = 'milestone'
                WHERE
                """+sqlCondition+"""
                  GROUP BY t.id
            """)
        print(sql)
        return db.session.execute(sql,filters).fetchone()
    except Exception as e:
        raise DatabaseError("根据皿ID和孔序号获取孔ID  ，再根据周期ID和孔ID 获取 胚胎ID异常",e.message,e)
        return None
    finally:
        db.session.remove()

def save(embryo):
    try :
        db.session.add(embryo)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('新增胚胎数据时发生错误', e.message, e)
    finally:
        db.session.remove()


def queryByProcedureIdAndCellId(procedureId,cellId):
    try:
        embryo = db.session.query(Embryo).filter(Embryo.procedureId == procedureId,Embryo.cellId == cellId).one_or_none()
    except Exception as e:
        return embryo
    finally:
        db.session.remove()
    return embryo
