from flask import Blueprint, render_template
import logUtils
from app import login_required

''' 主界面 '''
home_controller = Blueprint('home_controller', __name__)
url_prefix = '/front/home'

@home_controller.route('/', methods=['GET'])
@login_required
def main():
    logUtils.info('home_controller.main-跳转到主界面')
    return render_template('front/home.html')