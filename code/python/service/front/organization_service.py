# -*- coding: utf8 -*-
from common import uuid, logger, request_post
from app import conf, app_root
import json
import logUtils


def registerOrganization(args):
    try:
        if args["acloudId"] is None or args["acloudId"] == "":
            return 500, "医疗机构的aCloud ID不能为空"
        if args["acloudKey"] is None or args["acloudKey"] == "":
            return 500, "医疗机构的aCloud Key不能为空"
        if args["minioUser"] is None or args["minioUser"] == "":
            return 500, "医疗机构的minio用户名不能为空"
        if args["minioPass"] is None or args["minioPass"] == "":
            return 500, "医疗机构的minio密钥不能为空·"
        if len(args["minioPass"]) < 8:
            return 500, "医疗机构的minio密钥长度不能小于8·"
        code = "500"
        msg = "机构注册到云端失败，请稍后再试"
        data = {
            "acloudId": args["acloudId"],
            "acloudKey": args["acloudKey"],
            "s3Username": args["minioUser"],
            "s3Password": args["minioPass"],
        }
        logUtils.info(conf["ORGAN_REGISTER_URL"])
        res = request_post(conf["ORGAN_REGISTER_URL"], str(data))
        if res is not None:
            result = json.loads(res)
            if result["code"] == "200":
                # 写入JSON文件
                with open(app_root + conf["ORGAN_JSON_FILENAME"], "w") as fn:
                    fn.write(json.dumps(result["data"]))
            code = result["code"]
            msg = result["message"]
        return code, msg
    except:
        return 400, "机构注册到云端出现异常!"


"""
获取云端机构配置
"""


def getOrganConfig():
    try:
        # 获取JSON文件
        with open(app_root + conf["ORGAN_JSON_FILENAME"], "r") as fn:
            jstr = json.load(fn)
        if jstr is None:
            return None
        config = json.loads(jstr)
        return config
    except:
        return None
