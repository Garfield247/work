#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD


from .main import main
from .case import case
from .database import database
from .dbtable import dbtable
from .file import file
from .form import form
from .permission import permission
from .rights import rights
from .user import user
from .usergroup import usergroup
from .verifier import verifier
from .index import index
from .bi import bi
from .dataservice import ds
from .task import task
from .sql import sql

# 蓝本配置
DEFAULT_BLUEPRINT = (
    (main, "/"),
    (case, "/case"),
    (database, "/database"),
    (dbtable, "/dbtable"),
    (file, "/file"),
    (form, "/form"),
    (permission, "/permission"),
    (rights, "/rights"),
    (user, "/user"),
    (usergroup, "/usergroup"),
    (verifier, "/verifier"),
    (index, "/index"),
    (bi, "/bi"),
    (ds, "/ds"),
    (task, "/task"),
    (sql, "/sql"),
)


# 封装函数，完成蓝本注册
def config_blueprint(app):
    for blueprint, prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=prefix)
