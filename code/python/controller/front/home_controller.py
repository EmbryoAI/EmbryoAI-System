from flask import Blueprint, jsonify,render_template
from common import logger
from app import login_required 


''' 主界面 '''
home_controller = Blueprint('home_controller', __name__)
url_prefix = '/front/home'

@home_controller.route('/', methods=['GET'])
@login_required
def main():
    logger().info('进入home_controller.main主页面')
    return render_template('front/home.html')