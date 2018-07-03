# -*- coding: utf8 -*-

from flask import Blueprint
from flask_restful import reqparse
from common import logger
import service.front.embryo_service as embryo_service


embryo_rest_controller = Blueprint('embryo_rest_controller', __name__)
url_prefix = '/api/v1/embryo'


#根据procedureId查询胚胎列表
@embryo_rest_controller.route('/list/<string:id>', methods=['GET'])
def queryEmbryoList(id):
    return embryo_service.queryEmbryoList(id)