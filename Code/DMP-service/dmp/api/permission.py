#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import Blueprint, request

from dmp.models import Permissions, Users
from dmp.utils.put_data import PuttingData
from dmp.utils.response_hanlder import resp_hanlder, RET

permission = Blueprint("permission", __name__)


@permission.route("/all/", methods=["GET"], defaults={"desc": {"interface_name": "获取所有权限列表","is_permission": True,"permission_belong": 0}})
def all(desc):
    if request.method == 'GET':
        try:
            auth_token = request.headers.get('Authorization')
            res = PuttingData.get_obj_data(Users, auth_token)
            if not isinstance(res, dict):
                return resp_hanlder(code=999)
            # 获取当前所有权限信息
            permissions_all = Permissions.query.all()
            permissions_list = []
            for per_permission_obj in permissions_all:
                permissions_list.append(per_permission_obj)
            res_permission_list = [p.permission_to_dict() for p in permissions_list]
            return resp_hanlder(code=6001, msg=RET.alert_code[6001], result=res_permission_list)
        except Exception as err:
            resp_hanlder(code=999, msg=str(err))
