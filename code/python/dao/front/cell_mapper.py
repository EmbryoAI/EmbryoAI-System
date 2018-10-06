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
        cell = db.session.query(Cell).filter(Cell.dishId == dishId,Cell.cellCode == cellCode).one_or_none()
    except Exception as e:
        return cell
    finally:
        db.session.remove()
    return cell
