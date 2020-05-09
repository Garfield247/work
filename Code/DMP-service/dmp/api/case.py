#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from flask import Blueprint,jsonify

case = Blueprint("case",__name__)

@case.route("/all/",methods=["GET"],defaults={"desc":"案例列表"})
def all(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results":[
        {
        "id":1,
        "dmp_case_name":"lixian",
        "description":"lainxiandashuju",
        "url_name":"离线分析平台",
        "url":"http://www.xxxx.com",
        "data_table_count":10,
        "data_count":100000000,
        "created_on":"2020-03-18 15:00:00",
        "changed_on":"2020-03-28 15:00:00",
        },{
        "id":1,
        "dmp_case_name":"lixian",
        "description":"lainxiandashuju",
        "url_name":"离线分析平台",
        "Url":"http://www.xxxx.com",
        "data_table_count":10,
        "data_count":100000000,
        "created_on":"2020-03-18 15:00:00",
        "changed_on":"2020-03-28 15:00:00",
        }]}

    return jsonify(result)

@case.route("/post/",methods=["DEL"],defaults={"desc":"添加、修改案例"})
def cpost(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)

@case.route("/del/",methods=["DEL"],defaults={"desc":"删除案例"})
def cdel(desc):
    result = {
        "status": 0,
        "msg": "ok",
        "results": {
        }
    }
    return jsonify(result)


