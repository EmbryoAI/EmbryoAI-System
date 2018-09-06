# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class Rule(db.Model, mixin):
    __tablename__ = "t_rule"

    id = db.Column("id", db.String(32), primary_key=True, nullable=False)
    userId = db.Column("user_id", db.String(32))
    ruleName = db.Column("rule_name", db.String(100))
    description = db.Column("description", db.String(300))
    createTime = db.Column("create_time", db.DateTime)
    updateTime = db.Column("update_time", db.DateTime)
    delFlag = db.Column("del_flag", db.String(1))
    isDefault = db.Column("is_default", db.String(1))
    dataJson = db.Column("data_json", db.String(2048))