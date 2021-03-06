#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD

from flask import Blueprint,request, current_app
from dmp.models import Chart
from dmp.extensions import apscheduler
from dmp.utils.aps_task import task2json, update_chart_data
from dmp.utils.validators.task import Add_query_data_task_validator,Update_query_data_task_validator
from dmp.utils import resp_hanlder,uuid_str
from dmp.utils.engine import auto_connect

task = Blueprint("task",__name__)


# def update_chart_data(chart_id):
        # if Chart.exist_item_by_id(chart_id):
            # current_chart = Chart.get(chart_id)
            # data_table_id = current_chart.dmp_data_table_id
            # query_string = current_chart.query_string
            # conn = auto_connect(table_id=data_table_id)
            # if current_chart.data_table.dmp_database_type in [1, 2, 4]:
                # request_json = {
                    # "sql":eval(query_string).get("sql")
                        # }
                # _data = conn.exec_query(**request_json)
                # print(_data)
                # if type(_data) ==  list:
                    # field = eval(query_string).get("fields")

                    # current_chart.chart_data = [dict(zip(field , d)) for d in _data]
                    # print(current_chart.chart_data)
                    # current_chart.put()
                # return True,"OK"
        # else:
            # return False,"item not exist"





@task.route("/chart_data/<task_id>",methods=["GET"],defaults={"desc": {"interface_name": "查询单一任务信息", "is_permission": False, "permission_belong": None}})
def get_query_data_task(desc,task_id):
    """
    查询单一任务信息

    ---
    tags:
      - Task
    parameters:
      - name: task_id
        type: string
        required: true
        description: 任务ID
    responses:
      10:
        description: ok
	"""
    _task = apscheduler.get_job(id=task_id)
    return task2json(_task)

@task.route("/chart_data",methods=["POST"],defaults={"desc": {"interface_name": "添加图表更新任务", "is_permission": False, "permission_belong": None}})
def add_query_data_task(desc):
    """
    添加图表更新任务

    ---
    tags:
      - Task
    parameters:
      - name: chart_id
        type: int
        required: true
        description: 要添加定时更新任务的图表ID
      - name: time_unit
        type: string
        enum: ['weeks','days','hours','minutes','seconds']
        required: true
        description: 时间单位
      - name: time_value
        type: int
        required: true
        description: 时间数值
    responses:
      0:
        description: 添加定时任务成功并返回任务ID
    """
    _task_param = request.json
    valid = Add_query_data_task_validator(_task_param)
    if not valid.is_valid():
        return resp_hanlder(code=201,msg=valid.str_errors)
    chart_id = _task_param.get("chart_id")
    time_unit = _task_param.get("time_unit")
    time_value = _task_param.get("time_value")
    task_params = {}
    task_params["id"] = uuid_str()
    task_params["kwargs"] = {"chart_id":chart_id}
    task_params["func"] = update_chart_data
    task_params["trigger"] = "interval"
    task_params[time_unit] = time_value
    print(task_params)
    apscgeduler.add_job(**task_params)
    current_chart = Chart.get(chart_id)
    if current_chart:
        current_chart.update_task_id = task_params.get("id")
        current_chart.put()
    else:
        return resp_hanlder(code=999,msg="请确认查询正常并保存图表后再设定定时任务")

    return resp_hanlder(result={"task_id":task_params.get("id")})

@task.route("/chart_data/<task_id>",methods=["PUT"],defaults={"desc": {"interface_name": "修改图表更新任务", "is_permission": False, "permission_belong": None}})
def update_query_data_task(desc,task_id):
    """
    修改图表更新任务

    ---
    tags:
      - Task
    parameters:
      - name: time_unit
        type: string
        enum: ['weeks','days','hours','minutes','seconds']
        required: true
        description: 时间单位
      - name: time_value
        type: int
        required: true
        description: 时间数值
    responses:
      0:
        description: 修改成功
	"""
    current_task = apscheduler.get_job(task_id)
    if current_task:
        _task_param = request.json
        valid = Update_query_data_task_validator(_task_param)
        if not valid.is_valid():
            return resp_hanlder(code=201,msg=valid.str_errors)
        time_unit = _task_param.get("time_unit")
        time_value = _task_param.get("time_value")
        task_params = {}
        task_params["id"] = current_task.id
        task_params["trigger"] = "interval"
        task_params[time_unit] = time_value
        apscheduler.modify_job(**task_params)
        current_chart= Chart.query.filter_by(update_task_id=task_id).first()
        if current_chart:
            current_chart.update_task_id = task_params.get("id")
            current_chart.put()
        else:
            return resp_hanlder(code=999,msg="图表不存在或在操作期间被删除")
        return resp_hanlder(result="OK")
    else:
        return resp_hanlder(code=999,msg="任务不存在或已被删除")

@task.route("/chart_data/<task_id>",methods=["DELETE"],defaults={"desc": {"interface_name": "删除图表更新任务", "is_permission": False, "permission_belong": None}})
def delete_query_data_task(desc,task_id):
    """
    删除图表更新任务

    ---
    tags:
      - Task
    parameters:
      - name: task_id
        type: string
        required: true
        description: 要删除的定时更新任务的ID
    responses:
      0:
        description: 删除成功
	"""
    current_task = apscheduler.get_job(task_id)
    current_chart = Chart.query.filter_by(update_task_id=task_id).first()
    if current_task:
        current_task.remove()
        if current_chart:
            current_chart.update_task_id = None
            current_chart.put()
        else:
            return resp_hanlder(code=999,msg="图表不存在或在操作期间被删除")
        return resp_hanlder(result="OK")
    else:
        return resp_hanlder(code=999,msg="任务不存在或已删除")
