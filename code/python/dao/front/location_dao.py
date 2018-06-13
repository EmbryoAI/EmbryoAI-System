# -*- coding: utf8 -*-

from entity.Location import Location
from app import db

def getAllProvince():
    return db.session.query(Location).filter(Location.locationLevel == 0).all()

def getAllCitiesInProvince(provinceId):
    return db.session.query(Location).filter(Location.parentId == provinceId
        ).filter(Location.locationLevel == 1).all()

def getAllDistrictsInCity(cityId):
    return db.session.query(Location).filter(Location.parentId == cityId
        ).filter(Location.locationLevel == 2).all()