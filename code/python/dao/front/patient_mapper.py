from app import db
from entity.Procedure import Procedure
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc


def update(id, mobile, email):
    try:
        sql = text("UPDATE `t_patient` SET mobile = :mobile, email = :email WHERE id = :id")
        print(sql)
        db.session.execute(sql,{'id':id, 'mobile':mobile, 'email':email})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError("修改patient信息时发生错误",e.message,e)