# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db,login_manager
from flask_login import UserMixin


class User(UserMixin,db.Model,mixin):
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
    createTime = db.Column("create_time", db.DateTime)
    updateTime = db.Column("update_time", db.DateTime)
    lastLoginTime = db.Column("last_login_time", db.DateTime)
    delFlag = db.Column("del_flag", db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    if user_id is None:
        return None
    user = db.session.query(User).filter(User.id == id).one_or_none()
    if not user :
        return None
    return user
