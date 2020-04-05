# -*- coding: utf8 -*-

import dao.front.location_dao as locationDao


def getAllProvince():
    return locationDao.getAllProvince()


def getAllCitiesInProvince(provinceId):
    return locationDao.getAllCitiesInProvince(provinceId)


def getAllDistrictsInCity(cityId):
    return locationDao.getAllDistrictsInCity(cityId)
