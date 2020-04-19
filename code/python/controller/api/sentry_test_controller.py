from flask import Blueprint
from app import db
import logUtils
import service.front.dict_service as dict_service

sentry_test_controller = Blueprint("sentry_test_controller", __name__)
url_prefix = "/api/v1/sentry"


class CustomError(Exception):
    pass


@sentry_test_controller.route("/errortest", methods=["GET"])
def error_test():
    raise CustomError("This is for sentry.io test")


@sentry_test_controller.route("/sqlerror", methods=["GET"])
def sql_error():
    return db.session.execute("select * from non_exist_table").fetchall()
