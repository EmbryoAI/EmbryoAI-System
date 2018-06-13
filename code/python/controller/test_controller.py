from flask import Blueprint, jsonify
from common import logger
from flask import Flask, request, render_template
test_controller = Blueprint('test_controller', __name__,template_folder='templates1')
url_prefix = '/test'

@test_controller.route('/', methods=['GET'])
def test():
    logger().info('进入test_controller.test函数')
    return render_template('test/home.html')
 