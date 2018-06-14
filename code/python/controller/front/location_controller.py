# -*- coding: utf8 -*-

from flask import Blueprint, jsonify, render_template
from common import logger
from app import db
import service.front.location_service as locationService

location_controller = Blueprint('location_controller', __name__)
url_prefix = '/api/v1/location'

@location_controller.route('/province', methods=['GET'])
def getAllProvince():
    '''获取全国所有省、直辖市、自治区列表'''
    provinces = list(map(lambda x: x.to_dict(), locationService.getAllProvince()))
    return jsonify(provinces)

@location_controller.route('/province/<string:pid>/city')
def getAllCities(pid):
    '''获取某个省份、直辖市、自治区的城市列表'''
    cities = list(map(lambda x: x.to_dict(), locationService.getAllCitiesInProvince(pid)))
    return jsonify(cities)

@location_controller.route('/city/<string:cid>/district')
def getAllDistricts(cid):
    '''获取某个城市的区县列表'''
    districts = list(map(lambda x: x.to_dict(), locationService.getAllDistrictsInCity(cid)))
    return jsonify(districts)