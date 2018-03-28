from flask import Blueprint, jsonify
from common import logger

test1_controller = Blueprint('test1_controller', __name__)
url_prefix = '/test/test'

@test1_controller.route('/', methods=['GET'])
def test():
    logger().info('进入test1_controller.test函数')
    return 'ok'