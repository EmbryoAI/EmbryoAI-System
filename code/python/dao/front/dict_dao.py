from app import db
from entity.Dict import Dict
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc

def queryDictListByClass(dictClass):
    try:
        return db.session.query(Dict).filter(Dict.dictClass == dictClass).all()
    except Exception as e:
        raise DatabaseError("根据字典类型获取对应的字典列表失败!",e.message,e)
        return None
    finally:
        db.session.remove()

def queryDictListByClassS(dictClass):
#      articles = session.query(Article).filter(~Article.title.in_(['title2', 'title1'])).all()
    try:
        return db.session.query(Dict).filter(~Dict.dictClass.in_([dictClass])).all()
    except Exception as e:
        raise DatabaseError("根据多个字典类型获取对应的字典列表失败!",e.message,e)
        return None
    finally:
        db.session.remove()