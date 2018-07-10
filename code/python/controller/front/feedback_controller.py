from flask import Blueprint, jsonify,render_template
from common import logger
from app import login_required 
import service.front.feedback_service as feedback_service
from entity.Feedback import Feedback

''' 病历列表 '''

feedback_controller = Blueprint('feedback_controller', __name__)
url_prefix = '/front/feedback'

@feedback_controller.route('/return_visit/<string:id>', methods=['GET'])
@login_required
def return_visit(id):
    print(id)
    feedback = feedback_service.getFeedbackInfo(id)
    if not feedback:
        feedback = Feedback(procedureId=id)
    return render_template('front/procedure/return_visit.html', feedback=feedback)