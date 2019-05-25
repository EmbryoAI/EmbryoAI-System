from flask import Blueprint, jsonify,render_template
import logUtils
from app import login_required 
import service.front.feedback_service as feedback_service
from entity.Feedback import Feedback

''' 病历列表 '''

feedback_controller = Blueprint('feedback_controller', __name__)
url_prefix = '/front/feedback'

@feedback_controller.route('/return_visit/<string:id>', methods=['GET'])
@login_required
def return_visit(id):
    logUtils.info('feedback_controller.return_visit-跳转到病历回访页面')
    feedback = feedback_service.getFeedbackInfo(id)
    if not feedback:
        feedback = Feedback(procedureId=id)
    return render_template('front/procedure/return_visit.html', feedback=feedback)