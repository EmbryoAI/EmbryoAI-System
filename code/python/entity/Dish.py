# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class Dish(db.Model, mixin):
    __tablename__ = "sys_dish"

    id = db.Column("id", db.String(32), primary_key=True, nullable=False)
    incubatorId = db.Column("incubator_id", db.String(32))
    dishCode = db.Column("dish_code", db.String(3))
    createTime = db.Column("create_time", db.DateTime)
    updateTime = db.Column("update_time", db.DateTime)
    delFlag = db.Column("del_flag", db.Integer, default=0)
