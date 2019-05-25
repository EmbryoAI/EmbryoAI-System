# -*- coding: utf8 -*-

from entity.Location import Location
from app import db

def getAllProvince():
    try:
        return db.session.query(Location).filter(Location.locationLevel == 0).all()
    except Exception as e:
        raise DatabaseError("getAllProvince方法异常",e.message,e)
        return None
    finally:
        db.session.remove()

def getAllCitiesInProvince(provinceId):
    try:
        return db.session.query(Location).filter(Location.parentId == provinceId).filter(Location.locationLevel == 1).all()
    except Exception as e:
        raise DatabaseError("getAllCitiesInProvince方法异常",e.message,e)
        return None
    finally:
        db.session.remove()

def getAllDistrictsInCity(cityId):
    try:
        return db.session.query(Location).filter(Location.parentId == cityId).filter(Location.locationLevel == 2).all()
    except Exception as e:
        raise DatabaseError("getAllDistrictsInCity方法异常",e.message,e)
        return None
    finally:
        db.session.remove()