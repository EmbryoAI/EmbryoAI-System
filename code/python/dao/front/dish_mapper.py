from app import db
from entity.Dish import Dish
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc

def queryById(dishId):
    try:
        dish =  db.session.query(Dish).filter(Dish.id == dishId).one_or_none()
    except Exception as e:
        return dish
    finally:
        db.session.close()
    return dish

def findDishByIncubatorId(params):
    sql = text("""
        SELECT sd.id AS dishId,sd.dish_code AS dishCode, COUNT(te.cell_id) AS embryoCount
        FROM sys_dish sd
        LEFT JOIN sys_cell sc ON sd.id = sc.dish_id AND sc.del_flag = 0
        LEFT JOIN t_embryo te ON sc.id = te.cell_id AND sc.del_flag = 0
        WHERE sd.incubator_id = :incubatorId AND sd.del_flag = 0
        GROUP BY sc.dish_id
        """)
    print(sql)
    
    # 执行sql得出结果
    result = db.session.execute(sql,params)
    sql_result = result.fetchall()
    
    return sql_result

def findEmbryoSum(params):
    sql = text('''select sum(e.embryoCount) as embryoSum from (SELECT COUNT(te.cell_id) AS embryoCount
        FROM sys_dish sd
        LEFT JOIN sys_cell sc ON sd.id = sc.dish_id AND sc.del_flag = 0
        LEFT JOIN t_embryo te ON sc.id = te.cell_id AND sc.del_flag = 0
        WHERE sd.incubator_id = :incubatorId AND sd.del_flag = 0
        GROUP BY sc.dish_id) e''')
    print(sql)
    
    # 执行sql得出结果
    result = db.session.execute(sql,params)
    print(result)
    embryoSum = result.fetchone()[0]
    print(embryoSum)
    return embryoSum
 
