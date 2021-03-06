#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/11
# @Author  : SHTD

import re
import pymysql
from flask import current_app


class MysqlEngine():

    type=2
    def __init__(self, host, port, user, passwd, db):

        try:
            print(host)
            # current_app.logger.info(host, port, user, passwd, db)
            self.conn = pymysql.Connect(
                host=host, port=port, user=user, passwd=passwd, db=db)
            current_app.logger.info(self.conn.server_version)
        except Exception as e:
            current_app.logger.error(e)

    @property
    def tables_list(self):
        cursor = self.conn.cursor()
        sql = """
        show tables;
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        result = [i[0] for i in res]
        return result

    def columns(self, table_name):
        cursor = self.conn.cursor()
        sql = """

        Select COLUMN_NAME , DATA_TYPE  from INFORMATION_SCHEMA.COLUMNS Where table_name = '{table_name}';

        """
        cursor.execute(sql.format(table_name=table_name))
        _d = cursor.fetchall()
        columns_type_list = [
            {"dmp_data_table_column_name": str(column), "dmp_data_table_column_type": dtype} for column, dtype in _d]
        return columns_type_list

    def count(self, table_name):
        cursor = self.conn.cursor()
        sql = """
        Select count(*) from {table_name};
        """
        cursor.execute(sql.format(table_name=table_name))
        _count = cursor.fetchall()
        return int(_count[0][0])

    def execsql(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def exec_query(self,**kwages):
        sql =kwages.get("sql")
        if bool(re.match(r"^select ", sql, re.I)):
            cursor = self.conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            return res
        else:
            return "只能执行select 语句！"

    def retrieve(self, table_name, limit=100):
        cursor = self.conn.cursor()
        sql = """
        Select * from {table_name} limit {limit};
        """
        cursor.execute(sql.format(table_name=table_name, limit=limit))
        res = cursor.fetchall()
        return res

    def close_conn(self):
        self.conn.close()
