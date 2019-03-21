from app import db
from entity.Dish import Dish
from entity.Cell import Cell
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc

def save(cell):
    try :
        db.session.add(cell)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('新孔数据时发生错误', e.message, e)
    finally:
        db.session.remove()

def getCellByDishIdAndCellCode(dishId, cellCode):
    try:
        return db.session.query(Cell).filter(Cell.dishId == dishId,Cell.cellCode == cellCode).one_or_none()
    except Exception as e:
        return None
    finally:
        db.session.remove()

def queryCellByDishId(dishId):
    try:
        sql = text("""
                SELECT sc.`id` AS cell_id, sc.`cell_code` AS cell_code FROM `sys_cell` sc 
                WHERE sc.`dish_id` = '""" + dishId + """' 
            """)
        print(sql)
        return db.session.execute(sql).fetchall()
    except Exception as e:
        raise DatabaseError("根据皿ID查询孔信息异常",e.message,e)
        return None
    finally:
         db.session.remove()
