# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
from common import logger
import service.front.milestone_service as milestone_service
from app import login_required 

milestone_rest_controller = Blueprint('milestone_rest_controller', __name__)
url_prefix = '/api/v1/milestone'

#新增里程碑
@milestone_rest_controller.route('/add', methods=['POST'])
@login_required
def addMilestone():   
    code, milestone = milestone_service.insertMilestone(request)
    return make_response(jsonify(milestone), code)

#根据胚胎ID查询出里程碑相关信息
@milestone_rest_controller.route('/<string:embryoId>', methods=['GET'])
@login_required
def getMilestoneByEmbryoId(embryoId):
    return milestone_service.getMilestoneByEmbryoId(embryoId)