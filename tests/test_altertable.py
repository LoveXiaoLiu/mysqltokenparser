#!/usr/bin/env python
# coding:utf-8

import pytest
from helper import mysqltokenparser as mtp
from helper import constant as _c


def test_addcolumns():
    sql = u"ALTER TABLE tab_name ADD address01  varchar(100) NOT NULL \
        DEFAULT '' COMMENT '地址1' , ADD address02  varchar(100) NOT \
        NULL DEFAULT '' COMMENT '地址2', ADD INDEX \
        idx_eob_date(empid_org_bus (200),pfm_date),  ADD PRIMARY KEY (id);"

    tokens = mtp.mysql_token_parser(sql)
    assert isinstance(tokens, dict)

    hope_tablename = 'tab_name'
    assert hope_tablename == tokens['data']['data'][_c.TABLE_NAME]

    hope_add_len = 4
    assert hope_add_len == len(tokens['data']['data']['alter_data'])

    hope_columnname = ['address01', 'address02']
    assert tokens['data']['data']['alter_data'][0]['data'][_c.COLUMN_NAME] in hope_columnname
    assert tokens['data']['data']['alter_data'][1]['data'][_c.COLUMN_NAME] in hope_columnname


def test_addindexs():
    sql = u"ALTER TABLE t_a_gun2_6_dw_pfm_emp_cm ADD INDEX \
        idx_eob_date(empid_org_bus (200),pfm_date);"

    tokens = mtp.mysql_token_parser(sql)
    print(tokens)
    assert isinstance(tokens, dict)

    hope_tablename = 't_a_gun2_6_dw_pfm_emp_cm'
    assert hope_tablename == tokens['data']['data']['tablename']

    hope_indexname = 'idx_eob_date'
    assert hope_indexname == tokens['data']['data']['alter_data'][0]['data']['indexname']

    hope_columnname = ['empid_org_bus', 'pfm_date']
    assert hope_columnname == tokens['data']['data']['alter_data'][0]['data']['indexdefinition']['columnnames']


def test_adduniqueindexs():
    sql = u"ALTER TABLE tab_name ADD UNIQUE uniq_name (name(20), age);"

    tokens = mtp.mysql_token_parser(sql)
    print(tokens)
    assert isinstance(tokens, dict)

    hope_tablename = 'tab_name'
    assert hope_tablename == tokens['data']['data']['tablename']

    hope_indexname = 'uniq_name'
    assert hope_indexname == tokens['data']['data']['alter_data'][0]['data']['indexname']

    hope_columnname = ['name']
    assert hope_columnname == tokens['data']['data']['alter_data'][0]['data']['indexdefinition']['columnnames']


def test_altertable_dropcolumns():
    sql = u"ALTER TABLE tab_name DROP COLUMN address1, DROP COLUMN address2, DROP INDEX  uniq_name, DROP PRIMARY KEY;"

    tokens = mtp.mysql_token_parser(sql)
    print(tokens)
    assert isinstance(tokens, dict)

    hope_tablename = 'tab_name'
    assert hope_tablename == tokens['data']['data']['tablename']

    hope_drop_len = 2
    assert hope_drop_len == len(tokens['data']['data']['alter_data'])

    hope_columnname = ['address1', 'address2']
    assert tokens['data']['data']['alter_data'][0]['data']['columnname'] in hope_columnname
    assert tokens['data']['data']['alter_data'][1]['data']['columnname'] in hope_columnname


def test_modifycolumns():
    sql = u"ALTER TABLE tab_name MODIFY COLUMN amount bigint DEFAULT 0 COMMENT '数量',MODIFY COLUMN sumAmt bigint DEFAULT 0 COMMENT '总数量',MODIFY COLUMN  amount bigint DEFAULT 0 COMMENT 'name数量';"

    tokens = mtp.mysql_token_parser(sql)
    print(tokens)
    assert isinstance(tokens, dict)


def test_changecolumns():
    sql = u"ALTER TABLE tab_name  CHANGE  amount new_amount bigint DEFAULT 0 COMMENT 'name数量';"

    tokens = mtp.mysql_token_parser(sql)
    print(tokens)
    assert isinstance(tokens, dict)
