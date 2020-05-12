#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 


from dmp.extensions import db

class Permissions(db.Model):
    """权限表"""
    __tablename__ = 'dmp_permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='权限ID')
    route = db.Column(db.String(64), nullable=False, comment='权限路由')
    dmp_permission_name = db.Column(db.String(32), nullable=False, comment='路由功能名称')

    def __repr__(self):
        return self.dmp_permission_name

    def permission_to_dict(self):
        permission_dict = {
            'id': self.id,
            'route': self.route,
            'dmp_permission_name': self.dmp_permission_name
        }
        return permission_dict