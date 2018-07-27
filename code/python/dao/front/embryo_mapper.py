from app import db
from sqlalchemy import text
from entity.Embryo import Embryo

def queryEmbryoList(procedureID):
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
    
def getEmbryoById(id):

    return db.session.query(Embryo).filter(Embryo.id == id).one_or_none()

#动态条件查询里程碑对象
def getEmbryoById(id):
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