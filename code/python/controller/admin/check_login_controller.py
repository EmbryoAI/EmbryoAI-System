# -*- coding: utf8 -*-

from flask import Blueprint, render_template
from app import current_user

check_login_controller = Blueprint('check_login_controller', __name__)
url_prefix = '/'

@check_login_controller.route('/', methods=['GET'])
def main():
    if current_user.is_authenticated:
        return render_template('front/home.html', htmlType="incubator")
    return render_template('login.html')

