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