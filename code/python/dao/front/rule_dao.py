from app import db
from entity.Rule import Rule
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc


def insertRule(rule):
    try :
        db.session.add(rule)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('设置里程碑时发生错误!', e.message, e)
    finally:
        db.session.remove()
    
def updateRule(rule):
    try :
        sql = text("""
            UPDATE t_rule 
            SET
            user_id =:userId, 
            rule_name =:ruleName, 
            description =:description, 
            create_time =:createTime, 
            update_time =:updateTime, 
            del_flag =:delFlag, 
            is_default =:isDefault, 
            data_json =:dataJson
            WHERE id =:id
        """)
        
        db.session.execute(sql, rule.to_dict())
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('保存标准成功!', e.message, e)
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
        
def setDefault(ruleId,userId):
    try :
        #首先把当前用户的评分规则都设置为不默认
        sql = text("""
            UPDATE t_rule 
            SET is_default = 0
            WHERE user_id =:userId
        """)
        db.session.execute(sql, {"userId":userId})
        #再把当前规则设置为默认
        sql = text("""
            UPDATE t_rule 
            SET is_default = 1
            WHERE id =:ruleId
        """)
        db.session.execute(sql, {"ruleId":ruleId})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('保存标准成功!', e.message, e)
    finally:
        db.session.remove()

def findAllRules():
    return db.session.query(Rule)