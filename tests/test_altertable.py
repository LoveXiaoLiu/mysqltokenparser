#!/usr/bin/env python
# coding:utf-8

import pytest
from helper import mysqltokenparser as mtp


table_attr_map = mtp.TABLE_ATTR_MAP


def test_altertable_addcolumns():
    sql = u"ALTER TABLE tab_name ADD address01  varchar(100) NOT NULL \
        DEFAULT '' COMMENT '地址1' , ADD address02  varchar(100) NOT \
        NULL DEFAULT '' COMMENT '地址2' ;"

    token_obj = mtp.mysql_token_parser(sql)
    tokens = token_obj.get_tokens()

    assert isinstance(tokens, dict)

    hope_tablename = 'tab_name'
    tablename = tokens.get(table_attr_map.tablename)
    assert isinstance(tablename, list)
    assert hope_tablename in tablename

    hope_columns = ['address01', 'address02']
    columnnames = tokens.get(table_attr_map.columnnames)
    assert isinstance(columnnames, list)
    assert len(hope_columns) == len(columnnames)
    for col in hope_columns:
        assert col in columnnames

    hope_sqltype = 'ddl'
    sqltype = tokens.get(table_attr_map.sqltype)
    assert hope_sqltype in sqltype


def test_altertable_addindexs():
    sql = u"ALTER TABLE t_a_gun2_6_dw_pfm_emp_cm ADD INDEX \
        idx_eob_date(empid_org_bus (200),pfm_date);"

    token_obj = mtp.mysql_token_parser(sql)
    tokens = token_obj.get_tokens()
    assert isinstance(tokens, dict)

    hope_tablename = 't_a_gun2_6_dw_pfm_emp_cm'
    tablename = tokens.get(table_attr_map.tablename)
    assert isinstance(tablename, list)
    assert hope_tablename in tablename

    hope_columns = ['idx_eob_date']
    columnnames = tokens.get(table_attr_map.columnnames)
    assert isinstance(columnnames, list)
    assert len(hope_columns) == len(columnnames)
    for col in hope_columns:
        assert col in columnnames

    hope_indexs = ["empid_org_bus(200),pfm_date"]
    indexname = tokens.get(table_attr_map.indexname)
    for idx in hope_indexs:
        assert idx in indexname

    hope_sqltype = 'ddl'
    sqltype = tokens.get(table_attr_map.sqltype)
    assert hope_sqltype in sqltype
