#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import Blueprint, jsonify

rights = Blueprint("rights", __name__)


@rights.route("/all/", methods=["GET"], defaults={"desc": {"interface_name": "获取所有权利","is_permission": True,"permission_belong": 0}})
def all(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": [
            {
                "id": 1,
                "rights": "rights211"
            },
            {
                "id": 2,
                "rights": "rights2"
            }
        ]
    }
    return jsonify(result)
