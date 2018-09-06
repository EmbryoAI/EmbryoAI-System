from app import db
from entity.Rule import Rule
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

"""
  @see: 查询用户的规则列表
  @param userId: 用户ID
"""
def queryRuleListByUserId(userId):
    try:
        return db.session.query(Rule).filter(Rule.userId == userId).all()
    except Exception as e:
        raise DatabaseError("根据用户ID查询规则列表失败!",e.message,e)
        return None
    finally:
        db.session.remove()

"""
  @see: 查询用户的规则列表
  @param userId: 用户ID
"""
def getRuleById(ruleId,userId):
    try:
        return db.session.query(Rule).filter(Rule.userId == userId,Rule.id == ruleId).one_or_none()
    except Exception as e:
        raise DatabaseError("根据用户ID查询规则列表失败!",e.message,e)
        return None
    finally:
        db.session.remove()