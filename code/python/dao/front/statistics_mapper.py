from app import db
from entity.Procedure import Procedure
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc

def embryoOutcome(sqlCondition,filters):
#     pagination = Procedure.query.filter_by(**filters).order_by(Procedure.insemiTime.desc()).paginate(page,per_page=limit,error_out=False)
#     pagination = Procedure.query.filter_by(**filters).paginate(page,per_page=limit,error_out=False)
    sql = text("""
        SELECT COUNT(b.embryo_fate_id  ) 'count',a.dict_value AS 'name'
        FROM  sys_dict a 
        LEFT JOIN t_embryo b
        ON a.dict_key=b.embryo_fate_id  
        WHERE a.dict_class='embryo_fate_type'
        """+sqlCondition+"""
        GROUP BY a.dict_key
        """)
    print(sql)
    
    # 执行sql得出结果
    result = db.session.execute(sql,filters) 
    sql_result = result.fetchall()
  
    return sql_result

def milestoneEmbryos():
    sql = text("""
           SELECT COUNT(b.embryo_id) 'value',a.dict_value AS 'name' FROM sys_dict a
           LEFT JOIN t_milestone b
           ON a.dict_key=b.milestone_id
           LEFT JOIN t_embryo c
           ON b.embryo_id= c.id
           LEFT JOIN t_procedure d
           ON c.procedure_id = d.id AND d.cap_end_time IS NULL 
           WHERE a.dict_class='milestone'
           GROUP BY a.dict_key
       """)
    print(sql)
    
    # 执行sql得出结果
    result = db.session.execute(sql) 
    sql_result = result.fetchall()
  
    return sql_result


# SELECT 
#   CONCAT(FORMAT(SUM(CASE b.biochem_pregnancy WHEN '1' THEN 1 ELSE 0 END )/COUNT(a.id)*100,1),'%') AS 生化妊娠率,
#   CONCAT(FORMAT(SUM(CASE b.clinical_pregnancy WHEN '1' THEN 1 ELSE 0 END )/COUNT(a.id)*100,1),'%') AS 临床妊娠率,
#   CONCAT(FORMAT(SUM(CASE c.embryo_fate_id WHEN '1' THEN 1 ELSE 0 END )/COUNT(a.id)*100,1),'%')  临床着床率
# FROM t_procedure a
# JOIN t_feedback  b
# ON a.id=b.procedure_id
# JOIN t_embryo c
# ON a.id = c.procedure_id
