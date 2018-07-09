from flask import Blueprint, jsonify,render_template
from common import logger
from app import login_required 

''' 病历列表 '''

procedure_controller = Blueprint('procedure_controller', __name__)
url_prefix = '/front/procedure'

@procedure_controller.route('/', methods=['GET'])
@login_required
def main():
    logger().info('进入procedure_controller.procedure病历页面')
    return render_template('front/procedure/procedure.html',htmlType="incubator")

@procedure_controller.route('/<string:id>', methods=['GET'])
@login_required
def detail(id):
    logger().info('进入procedure_controller.procedure病历详情页面')
    return render_template('front/procedure/detail.html', id=id)