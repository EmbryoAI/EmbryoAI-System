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