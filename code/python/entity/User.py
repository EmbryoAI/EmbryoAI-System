# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class User(db.Model, mixin):
    __tablename__ = "sys_user"

    id = db.Column("id", db.String(32), primary_key=True, nullable=False)
    username = db.Column("username", db.String(50))
    password = db.Column("password", db.String(20))
    email = db.Column("email", db.String(200))
    mobile = db.Column("mobile", db.String(30))
    truename = db.Column("truename", db.String(50))
    title = db.Column("title", db.String(50))
    isAdmin = db.Column("is_admin", db.Integer, default=0)
    isPrivate = db.Column("is_private", db.Integer, default=0)
    sex = db.Column("sex", db.String(30))
    birthday = db.Column("birthday", db.Integer)
    createTime = db.Column("create_time", db.DateTime)
    updateTime = db.Column("update_time", db.DateTime)
    lastLoginTime = db.Column("last_login_time", db.DateTime)
    delFlag = db.Column("del_flag", db.Integer, default=0)

