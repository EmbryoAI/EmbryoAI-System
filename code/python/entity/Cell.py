# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class Cell(db.Model, mixin):
    __tablename__ = "sys_cell"

    id = db.Column("id", db.String(32), primary_key=True, nullable=False)
    dishId = db.Column("dish_id", db.String(32))
    cellCode = db.Column("cell_code", db.String(3))
    createTime = db.Column("create_time", db.DateTime)
    updateTime = db.Column("update_time", db.DateTime)
    delFlag = db.Column("del_flag", db.Integer, default=0)
