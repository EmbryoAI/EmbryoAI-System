# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class Log(db.Model, mixin):
    __tablename__ = "sys_log"

    id = db.Column("id", db.String(32), primary_key=True, nullable=False)
    userId = db.Column("user_id", db.String(32))
    crudOp = db.Column("crud_op", db.String(2))
    tableName = db.Column("table_name", db.String(50))
    sqlCommand = db.Column("sql_command", db.String(500))
    opTime = db.Column("op_time", db.DateTime)
    logMessage = db.Column("log_message", db.String(255))

