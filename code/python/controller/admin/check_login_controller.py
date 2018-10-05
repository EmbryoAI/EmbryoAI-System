# -*- coding: utf8 -*-

from flask import Blueprint, jsonify,render_template,request, make_response, abort,session
from flask_restful import reqparse
import service.admin.user_service as user_service
from entity.User import User
import time
import hashlib
from common import logger
from app import login_manager,login_user, logout_user, login_required,current_user

check_login_controller = Blueprint('check_login_controller', __name__)
url_prefix = '/'

@check_login_controller.route('/', methods=['GET'])
def main():
    if current_user.is_authenticated:
        return render_template('front/home.html',htmlType="incubator")
    return render_template('login.html')

