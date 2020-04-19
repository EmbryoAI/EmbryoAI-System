from sqlalchemy.exc import DatabaseError
from app import db
import logUtils as logger
from entity.Dict import Dict


def queryDictListByClass(dictClass):
    try:
        return db.session.query(Dict).filter(Dict.dictClass == dictClass).all()
    except Exception as e:
        logger.error("根据字典类别获取对应的字典列表发生错误: {e}")
        raise DatabaseError("根据字典类别获取对应的字典列表发生错误", e.message, e)
    finally:
        db.session.remove()


def queryDictListByClassS(dictClass):
    #      articles = session.query(Article).filter(~Article.title.in_(['title2', 'title1'])).all()
    try:
        return db.session.query(Dict).filter(~Dict.dictClass.in_([dictClass])).all()
    except Exception as e:
        logger.error("根据逗号隔开多个字典类别获取列表发生错误: {e}")
        raise DatabaseError("根据逗号隔开多个字典类别获取列表发生错误!", e.message, e)
    finally:
        db.session.remove()


def queryDictListByDictParentId(dictParentId):
    try:
        return db.session.query(Dict).filter(Dict.dictParentId == dictParentId).all()
    except Exception as e:
        logger.error("根据父级字典ID获取子集字典列表发生错误: {e}")
        raise DatabaseError("根据父级字典ID获取子集字典列表发生错误!", e.message, e)
    finally:
        db.session.remove()


def getDictByClassAndKey(dictClass, dictKey):
    #      articles = session.query(Article).filter(~Article.title.in_(['title2', 'title1'])).all()
    try:
        return (
            db.session.query(Dict)
            .filter(Dict.dictClass == dictClass, Dict.dictKey == dictKey)
            .one_or_none()
        )
    except Exception as e:
        logger.error("根据逗号隔开多个字典类别获取列表发生错误: {e}")
        raise DatabaseError("根据逗号隔开多个字典类别获取列表发生错误!", e.message, e)
    finally:
        db.session.remove()
