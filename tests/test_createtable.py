#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mysqltokenparser` package."""

import pytest


from helper import mysqltokenparser as mtp


table_attr_map = mtp.TABLE_ATTR_MAP


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_createtable(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

    sql = u"""
            CREATE TABLE `aaa`.`t_zcm_operation_luck_award_record` (
      `id` bigint(20) NOT NULL,
      `operation_seq` varchar(30) NOT NULL,
      `award_user_id` bigint(20) NOT NULL,
      `award_type` int(11) DEFAULT NULL,
      `award_id` varchar(40) DEFAULT NULL UNIQUE KEY,
      `award_content` varchar(20)  DEFAULT NULL,
      `award_reason` varchar(30)  DEFAULT NULL,
      `award_source` int(11) DEFAULT NULL,
      `state` tinyint(4) NOT NULL PRIMARY KEY,
      `addtime` datetime NOT NULL,
      `updatetime` datetime NOT NULL,
      `ip` varchar(50)  DEFAULT NULL,
      `imei` varchar(50)  DEFAULT NULL,
      `intext` int(11) DEFAULT NULL,
      `longext` bigint(20) DEFAULT NULL,
      `strext` varchar(200)  DEFAULT NULL,
      PRIMARY KEY (id),
      UNIQUE KEY `idx_op_seq_uid_type` (`operation_seq`,`award_user_id`,`award_type`),
      KEY `idx_op_uid_type` (`award_user_id`,`award_type`),
      KEY `idx_op_uid_sss` (longext(10))
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """

    token_obj = mtp.mysql_token_parser(sql)
    tokens = token_obj.get_tokens()
    assert isinstance(tokens, dict)

    hope_tablename = "aaa.t_zcm_operation_luck_award_record"
    tablename = tokens.get(table_attr_map.tablename)
    assert isinstance(tablename, list)
    assert hope_tablename in tablename

    hope_columnnames = [
        u'id', u'operation_seq', u'award_user_id', u'award_type',
        u'award_id', u'award_content', u'award_reason', u'award_source',
        u'state', u'addtime', u'updatetime', u'ip', u'imei', u'intext', u'longext', u'strext'
    ]
    columnnames = tokens.get(table_attr_map.columnnames)
    assert isinstance(columnnames, list)
    assert len(columnnames) == len(hope_columnnames)
    for hc in hope_columnnames:
        assert hc in columnnames

    hope_sqltype = 'ddl'
    sqltype = tokens.get(table_attr_map.sqltype)
    assert hope_sqltype in sqltype
