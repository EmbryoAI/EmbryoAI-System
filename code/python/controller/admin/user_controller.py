from flask import Blueprint, jsonify,render_template
from common import logger

''' 后台增删查改demo '''

user_controller = Blueprint('user_controller', __name__)
url_prefix = '/admin/user'

@user_controller.route('/', methods=['GET'])
def main():
    return render_template('admin/user/user_manage.html')

'''分页查询数据'''
@user_controller.route('/list/', methods=['GET'])
def list():
    return '{"code":0,"msg":"","count":1000,"data":[{"id":10000,"username":"user-0","sex":"女","city":"城市-0","sign":"签名-0","experience":255,"logins":24,"wealth":82830700,"classify":"作家","score":57}]}'

''' 跳转到添加页面 '''
@user_controller.route('/toAdd/', methods=['GET'])
def toAdd():
    return render_template('admin/user/add.html')

