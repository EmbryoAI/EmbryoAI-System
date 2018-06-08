# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class ProcedureDish(db.Model, mixin):
    __tablename__ = "t_procedure_dish"

    id = db.Column("id", db.String(32), primary_key=True, nullable=False)
    procedureId = db.Column("procedure_id", db.String(32))
    dishId = db.Column("dish_id", db.String(32))
    imagePath = db.Column("image_path", db.String(500))

