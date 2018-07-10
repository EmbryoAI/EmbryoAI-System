
from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
from common import logger
from app import db
import service.front.statistics_service as statistics_service
from entity.User import User
import time
from app import login_required 

statistics_rest_controller = Blueprint('statistics_rest_controller', __name__)
url_prefix = '/api/v1/statistics'


#时间范围胚胎结局统计
@statistics_rest_controller.route('/embryo/outcome', methods=['GET'])
@login_required
def embryoOutcome():
    logger().info('进入statistics_controller.embryoOutcome胚胎结局统计')
    return statistics_service.embryoOutcome(request)





