from app import db
from sqlalchemy import text


def queryEmbryoList(procedureID):
    sql = text("""
        SELECT t.`embryo_index`, sc.`cell_code`, sd.`dish_code`, si.`incubator_code` 
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