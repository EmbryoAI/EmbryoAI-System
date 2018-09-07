from flask import Blueprint, jsonify,render_template
from common import logger
from app import login_required 
from flask_restful import reqparse

''' 病历列表 '''

procedure_controller = Blueprint('procedure_controller', __name__)
url_prefix = '/front/procedure'

@procedure_controller.route('/', methods=['GET'])
@login_required
def main():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    agrs = parser.parse_args()
    name = agrs['name']
    if name is None :
        name = ""

    logger().info('进入procedure_controller.procedure病历页面')
    return render_template('front/procedure/procedure.html',htmlType="incubator",name=name)

@procedure_controller.route('/view', methods=['GET'])
@login_required
def view():
    logger().info('进入procedure_controller.procedureView胚胎周期视图页面')
    return render_template('front/procedure/procedureView.html',htmlType="incubator")

@procedure_controller.route('/<string:id>', methods=['GET'])
@login_required
def detail(id):
    logger().info('进入procedure_controller.procedure病历详情页面')
    return render_template('front/procedure/detail.html', id=id)

@procedure_controller.route('/return_visit/<string:id>', methods=['GET'])
@login_required
def return_visit(id):
    return render_template('front/procedure/return_visit.html', id=id)

#去新建病理页面
@procedure_controller.route('/add', methods=['GET'])
@login_required
def add():
    return render_template('front/procedure/createCase.html')