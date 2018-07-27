from app import db
from entity.Dict import Dict
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc

def queryDictListByClass(dictClass):
    return db.session.query(Dict).filter(Dict.dictClass == dictClass).all()

def queryDictListByClassS(dictClass):
#      articles = session.query(Article).filter(~Article.title.in_(['title2', 'title1'])).all()
    return db.session.query(Dict).filter(~Dict.dictClass.in_([dictClass])).all()