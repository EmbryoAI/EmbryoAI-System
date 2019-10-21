from flask import Blueprint, render_template
from flask_restful import reqparse
import logUtils
from app import login_required

''' 病历列表 '''

procedure_controller = Blueprint('procedure_controller', __name__)
url_prefix = '/front/procedure'

@procedure_controller.route('/', methods=['GET'])
@login_required
def main():
    logUtils.info('procedure_controller.main-跳转到病历页面')
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    args = parser.parse_args()
    name = args['name'] if args['name'] else ''
    # if name is None :
    #     name = ""
    return render_template('front/procedure/procedure.html',
        htmlType="incubator", name=name)

@procedure_controller.route('/view', methods=['GET'])
@login_required
def view():
    logUtils.info('procedure_controller.view-跳转到胚胎周期视图页面')
    parser = reqparse.RequestParser()
    parser.add_argument('medicalRecordNo', type=str)
    args = parser.parse_args()
    medicalRecordNo = args['medicalRecordNo']
    return render_template('front/procedure/procedureView.html',
        htmlType="incubator", medicalRecordNo=medicalRecordNo)

@procedure_controller.route('/<string:id>', methods=['GET'])
@login_required
def detail(id):
    logUtils.info('procedure_controller.detail-跳转到病历详情页面')
    return render_template('front/procedure/detail.html', id=id)

@procedure_controller.route('/return_visit/<string:id>', methods=['GET'])
@login_required
def return_visit(id):
    logUtils.info('procedure_controller.return_visit-跳转到病历回访页面')
    return render_template('front/procedure/return_visit.html', id=id)

#去新建病理页面
@procedure_controller.route('/add', methods=['GET'])
@login_required
def add():
    logUtils.info('procedure_controller.add-跳转到新建病理页面')
    return render_template('front/procedure/createCase.html')