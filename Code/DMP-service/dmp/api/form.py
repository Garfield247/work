#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD
import os

from flask import Blueprint, jsonify, request, current_app
from dmp.models import FromUpload,FromMigrate,FromDownload,FromAddDataTable,Users,DataTable,Database
from dmp.utils import resp_hanlder
from dmp.utils.datax_job_hanlder import mysql_reader,mysql_writer,mongodb_reader,mongodb_writer,hive_reader,hive_writer
from dmp.utils.job_task import job_hanlder
from dmp.api.dbtable import post
from dmp.engine import auto_connect

form = Blueprint("form",__name__)

@form.route("/formdb/",methods=["POST"],defaults={"desc":"从数据库添加数据表的表单"})
def from_db(desc):
    if request.method == "POST":
        try:
            form_info = request.json
            data_tablename = form_info.get("data_tablename")
            db_tablename = form_info.get("db_tablename")
            database_id = form_info.get("database_id")
            dmp_data_case_id = form_info.get("dmp_data_case_id")
            description = form_info.get("description")
            submit_dmp_user_id = 3
            new_form = FromAddDataTable(
                dmp_data_table_name = data_tablename,
                db_table_name = db_tablename,
                dmp_database_id = database_id,
                dmp_case_id = dmp_data_case_id,
                description = description,
                submit_dmp_user_id = submit_dmp_user_id,
                )
            new_form.save()
            current_app.logger.info(new_form.id)
            return resp_hanlder(result="OK")
        except Exception as err:
            return resp_hanlder(code=999,err=err)


@form.route("/formfile/",methods=["POST"],defaults={"desc":"从文件添加数据表的表单"})
def from_file(desc):
    if request.method == "POST":
        try:
            form_info = request.json
            filetype = form_info.get("filetype")
            filepath = form_info.get("filepath")
            column_line = form_info.get("column_line")
            column = form_info.get("column")
            json_dimension_reduction = form_info.get("json_dimension_reduction")
            destination_dmp_datebase_id = form_info.get("destination_dmp_datebase_id")
            tablename = form_info.get("tablename")
            method = form_info.get("method")
            dmp_data_case_id = form_info.get("dmp_data_case_id")
            description = form_info.get("description")
            submit_dmp_user_id = 3
            new_form = FromUpload(
                filetype = filetype,
                filepath = filepath,
                column_line = column_line,
                column = column,
                json_dimension_reduction = json_dimension_reduction,
                destination_dmp_datebase_id = destination_dmp_datebase_id,
                new_tablename = tablename,
                method = method,
                dmp_data_case_id = dmp_data_case_id,
                description = description,
                submit_dmp_user_id = submit_dmp_user_id,
                )
            new_form.add()
            current_app.logger.info(new_form.id)
            return resp_hanlder(result="OK")
        except Exception as err:
            return resp_hanlder(code=999,err=err)

@form.route("/migration/",methods=["POST"],defaults={"desc":"数据迁移表单"})
def migration(desc):

    if request.method == "POST":
        try:
            form_info = request.json
            origin_dmp_table_id = form_info.get("origin_dmp_table_id")
            rule = form_info.get("rule")
            destination_dmp_database_id = form_info.get("destination_dmp_database_id")
            new_table_name = form_info.get("new_table_name")
            method = form_info.get("method")
            description = form_info.get("description")
            submit_dmp_user_id = 3
            new_form = FromMigrate(
                origin_dmp_table_id = origin_dmp_table_id,
                rule = rule,
                destination_dmp_database_id = destination_dmp_database_id,
                new_table_name = new_table_name,
                method = method,
                description = description,
                submit_dmp_user_id = submit_dmp_user_id,
                )
            current_app.logger.info(new_form.__json__())
            new_form.save()
            current_app.logger.info(new_form.id)
            return resp_hanlder(result="OK")
        except Exception as err:
            return resp_hanlder(code=999,err=err)

@form.route("/download/",methods=["POST"],defaults={"desc":"文件下载表单"})
def download(desc):

    if request.method == "POST":
        try:
            form_info = request.json
            dmp_table_id = form_info.get("dmp_table_id")
            rule = form_info.get("rule")
            destination_dmp_datebase_id = form_info.get("destination_dmp_datebase_id")
            description = form_info.get("description")
            submit_dmp_user_id = 3
            new_form = FromDownload(
                dmp_table_id = dmp_table_id,
                rule = rule,
                destination_dmp_datebase_id = destination_dmp_datebase_id,
                description = description,
                submit_dmp_user_id = submit_dmp_user_id,
                )
            new_form.add()
            current_app.logger.info(new_form.id)
            return resp_hanlder(result="OK")
        except Exception as err:
            return resp_hanlder(code=999,err=err)

def form_permission(user_id):
    if user_id:
        return 3

@form.route("/info/",methods=["GET"],defaults={"desc":"获取表单信息"})
def info(desc):
    if request.method == "GET":
        forms = [FromAddDataTable,
                FromUpload,
                FromMigrate,
                FromDownload,]
        user_id = 2
        try:
            committed,pending,complete = [],[],[]
            if form_permission(user_id) == 1:
                for _form in forms:
                    committed.extend([f.__json__() for f in _form.query.filter_by(submit_dmp_user_id=user_id,approve_result=0).all()])
                    complete.extend([f.__json__() for f in _form.query.filter(_form.submit_dmp_user_id==user_id,_form.approve_result!=0).all()])
                return resp_hanlder(result={"comiitted":committed,"complete":complete})
            elif form_permission(user_id) == 2:
                for _form in forms:
                    committed.extend([f.__json__() for f in _form.query.filter_by(submit_dmp_user_id=user_id,approve_result=0).all()])
                    pending.extend([f.__json__()  for f in _form.query.filter_by(submit_dmp_user_id=u.id,approve_result=0).all() for u in Users.query.filter_by(leader_dmp_user_id=user_id).all()] )
                    complete.extend([f.__json__() for f in _form.query.filter(_form.submit_dmp_user_id==user_id or _form.approve_dmp_user_id==user_id,_form.approve_result!=0).all()])
                return resp_hanlder(result={"comiitted":committed,"pending":pending,"complete":complete})
            elif form_permission(user_id) == 3:
                for _form in forms:
                    pending.extend([f.__json__()  for f in _form.query.filter_by(approve_result=0).all() ] )
                    complete.extend([f.__json__() for f in _form.query.filter(_form.approve_result!=0).all()])
                return resp_hanlder(result={"pending":pending,"complete":complete})
        except Exception as err:
            return resp_hanlder(code=999,err=err)



@form.route("/approve/",methods=["PUT"],defaults={"desc":"表单审批"})
def approve(desc):
    if request.method == "PUT":
        try:
            approve_form_info = request.json
            auth_token = request.headers.get('Authorization')
            approve_user_id = Users.decode_auth_token(auth_token)
            form_type = approve_form_info.get("dmp_form_type",None)
            form_id = approve_form_info.get("dmp_form_id",None)
            approve_result = approve_form_info.get("approve_result",None)
            answer = approve_form_info.get("answer",None)

            if form_type == 1:
                # 从数据库添加数据表单
                approve_form = FromAddDataTable.get(form_id)
                approve_form.approve_dmp_user_id = approve_user_id
                approve_form.approve_result=approve_result
                approve_form.answer = answer
                if approve_result == 1:
                    post(
                        dmp_data_table_name=approve_form.dmp_data_table_name,
                        db_table_name=approve_form.db_table_name,
                        dmp_user_id=approve_form.submit_dmp_user_id,
                        dmp_database_id=approve_form.dmp_database_id,
                        dmp_case_id=approve_form.dmp_case_id,
                        description=approve_form.description
                        )
                approve_form.put()
                return resp_hanlder(result="OK!")
            elif form_type == 2:
                # 文件上传添加数据表单
                approve_form = FromUpload.get(form_id)
                approve_form.approve_dmp_user_id = approve_user_id
                approve_form.approve_result=approve_result
                approve_form.answer = answer

                file_path = os.path.join(current_app.config.get("UPLOADED_PATH"),approve_form.file_path)
                filetype = approve_form.get("filetype")
                filepath = approve_form.get("filepath")
                column_line = approve_form.get("column_line")
                column = approve_form.get("column")
                json_dimension_reduction = approve_form.get("json_dimension_reduction")
                destination_dmp_datebase_id = approve_form.get("destination_dmp_datebase_id")
                tablename = approve_form.get("tablename")
                method = approve_form.get("method")
                dmp_data_case_id = approve_form.get("dmp_data_case_id")
                if approve_form.file_type == 1:
                    # csv

                    pass
                elif approve_form.file_type == 2:
                    # json
                    pass
                elif approve_form.file_type == 3:
                    #excel
                    pass
                else:
                    return resp_hanlder(code=999)
            elif form_type == 3:
                # 数据迁移表单
                approve_form = FromMigrate.get(form_id)
                approve_form.approve_dmp_user_id = approve_user_id
                approve_form.approve_result=approve_result
                approve_form.answer = answer
                if approve_result == 1:
                    origin_data_table = DataTable.get(approve_form.origin_dmp_table_id)
                    origin_database = Database.get(origin_data_table.dmp_database_id)
                    origin_database_type = origin_database.db_type
                    origin_db_host = origin_database.db_host
                    origin_db_port = origin_database.db_port
                    origin_db_username = origin_database.db_username
                    origin_db_passwd = origin_database.db_passwd
                    origin_db_name = origin_database.db_name
                    origin_db_table_name = origin_data_table.db_table_name

                    destination_database = Database.get(approve_form.destination_dmp_database_id)
                    destination_database_type = destination_database.db_type
                    destination_db_host =  destination_database.db_host
                    destination_db_port =  destination_database.db_port
                    destination_db_username =  destination_database.db_username
                    destination_db_passwd =  destination_database.db_passwd
                    destination_db_name =  destination_database.db_name
                    destination_db_table_name =  approve_form.new_table_name

                    rule = approve_form.rule
                    method = approve_form.method
                    base_column = auto_connect(origin_data_table.dmp_database_id).columns(origin_data_table.db_table_name)
                    # current_app.logger.info(base_column)
                    reader= []
                    if origin_database_type == 1:
                        # hive_reader
                        reader = hive_reader(host=origin_db_host,
                        port = origin_db_port,
                        path = None,
                        fileType=None,
                        haveKerberos=None,
                        kerberosKeytabFilePath=None,
                        kerberosPrincipal=None,
                        column=[],
                        fieldDelimiter=',',
                        encoding="utf-8"
                        )
                    elif origin_database_type == 2:
                        # mysql_reader
                        column = [col.get("dmp_data_table_column_name") for col in base_column]
                        reader = mysql_reader(username=origin_db_username,
                        password=origin_db_passwd,
                        column=column,
                        host=origin_db_host,
                        port=origin_db_port,
                        db=origin_db_name,
                        table=origin_db_table_name,
                        where=None,
                        # querySql=None
                        )

                    elif origin_database_type == 3:
                        # mongodb
                        column = [{"index":i+1,"name":col.get("dmp_data_table_column_name"),"type":col.get("dmp_data_table_column_type")} for i,col in enumerate(base_column)]
                        reader = mongodb_reader(host=origin_db_host,
                        port=origin_db_port,
                        db_name=origin_db_name,
                        collection_name=origin_db_table_name,
                        column=column,
                        username=origin_db_username,
                        password=origin_db_passwd
                        )
                        pass
                    writer = []
                    if destination_database_type == 1:
                        # hive_writer
                        writer = hive_writer(host=destination_db_host,
                        port=destination_db_port,
                        path=None,
                        filename=None,
                        column=[],
                        fieldDelimiter=",",
                        )
                        pass
                    elif destination_database_type == 2:
                        # myqsl_writer
                        column = [col.get("dmp_data_table_column_name") for col in base_column]
                        writer = mysql_writer(model=method,
                        username=destination_db_username,
                        password=destination_db_passwd,
                        column=column,
                        host=destination_db_host,
                        port=destination_db_port,
                        db=destination_db_name,
                        table=destination_db_table_name,
                        preSql=None,
                        postSql=None,
                        )
                    elif destination_database_type == 3:
                        # mongo_writer
                        column = [{"name": col.get("dmp_data_table_column_name")} for col in base_column]
                        writer = mongodb_writer(host=destination_db_host,
                        port=destination_db_port,
                        username=destination_db_username,
                        password=destination_db_passwd,
                        db_name=destination_db_name,
                        collection_name=destination_db_table_name,
                        column=column,
                        )

                    job_hanlder.delay(reader= reader,writer=writer)
                approve_form.put()
                return resp_hanlder(result="OK!")
                pass
            elif form_type == 4:
                # 数据下载表单
                pass
        except Exception as err:
            return resp_hanlder(code=999,err=err)
