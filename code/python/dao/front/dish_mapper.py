from app import db
from entity.Dish import Dish
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc

def queryById(dishId):
    return db.session.query(Dish).filter(Dish.id == dishId).one_or_none()