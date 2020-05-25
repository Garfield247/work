#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/25
# @Author  : SHTD 


import os
from flask import current_app
from dmp.datax_job_hanlder import *
def test():
    r = mongodb_reader(host="192.168.3.119",port=27017,db_name="case01",collection_name="yingcai_data",username=None,password=None)
    w = mysql_writer(model=1,host="192.168.3.87",port=3306,username="root",password="shtd123.",column=None,db="database",table="test_yc",preSql=None,postSql=None)
    job_jsonpath = job_hanlder(reader=r,writer=w)

    os.system("/usr/bin/python2.7 /home/dmp/datax/bin/datax.py %s"%job_jsonpath)