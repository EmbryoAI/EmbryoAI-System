from flask import Blueprint, jsonify,render_template
from common import logger
from app import login_required 

''' 统计模块 '''

statistics_controller = Blueprint('statistics_controller', __name__)
url_prefix = '/front/statistics'

@statistics_controller.route('/', methods=['GET'])
@login_required
def main():
    logger().info('进入statistics_controller.statistics统计页面')
    return render_template('front/statistics/statistics.html',htmlType="statistics")