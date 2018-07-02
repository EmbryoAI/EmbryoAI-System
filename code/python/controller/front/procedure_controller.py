from flask import Blueprint, jsonify,render_template
from common import logger

''' 病历列表 '''

procedure_controller = Blueprint('procedure_controller', __name__)
url_prefix = '/front/procedure'

@procedure_controller.route('/', methods=['GET'])
def main():
    logger().info('进入procedure_controller.procedure病历页面')
    return render_template('front/procedure/procedure.html',htmlType="incubator")