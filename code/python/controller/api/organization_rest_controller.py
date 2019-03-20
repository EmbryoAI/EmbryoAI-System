# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,request, make_response
from flask_restful import reqparse
from common import request_post
import json
from app import app_root,conf
import service.front.organization_service as organization_service

organization_rest_controller = Blueprint('organization_rest_controller', __name__)
url_prefix = '/api/v1/organization'

# 注册到云端接口
@organization_rest_controller.route('/registerToCloud', methods=['get','post'])
def registerToCloud():
    parser = reqparse.RequestParser()
    parser.add_argument('acloudId', type=str)
    parser.add_argument('acloudKey', type=str)
    parser.add_argument('minioUser', type=str)
    parser.add_argument('minioPass', type=str)
    args = parser.parse_args()
    code,message = organization_service.registerOrganization(args)
    return make_response(message, code)


