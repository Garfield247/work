#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

import datetime
from dmp.extensions import db
from dmp.models import DMPModel


class Case(db.Model, DMPModel):
    """案例表"""
    __tablename__ = 'dmp_case'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dmp_case_name = db.Column(db.String(32), nullable=False, comment='案例名称')
    description = db.Column(db.Text, comment='案例说明')
    url_name = db.Column(db.String(32), comment='可视化网站名称')
    url = db.Column(db.String(64), comment='网址')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')

    def delete(self):
        from dmp.models import DataTable
        case_table_count = DataTable.query.filter_by(dmp_case_id = self.id).count()
        if case_table_count == 0:
            db.session.delete(self)
        elif case_table_count > 0 :
            raise Exception("This case contains a data table and cannot be deleted!")
