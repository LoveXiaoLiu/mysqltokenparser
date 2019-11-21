#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mysqltokenparser` package."""

import pytest

from helper import mysqltokenparser as mtp
from helper import constant as _c


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
            CREATE TABLE tab_name (
  id    int         NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
  uid   int(2)         NOT NULL COMMENT '唯一流水id',
  okmysite  DECIMAL(6,2)   NOT NULL COMMENT 'cccc',
  name  varchar(20) NOT NULL DEFAULT '' COMMENT '名称',
  amount    DOUBLE(6,2)         NOT NULL DEFAULT 0 COMMENT '数量',
  create_date   date        NOT NULL DEFAULT '1000-01-01' COMMENT '创建日期',
  create_time   datetime    DEFAULT '1000-01-01 00:00:00' COMMENT '创建时间',
  update_time   timestamp   default current_timestamp on update current_timestamp COMMENT '更新时间(会自动更新，不需要刻意程序更新)',
  PRIMARY KEY (id),
  UNIQUE KEY uniq_uid (uid, ccccc),
  KEY idx_name (name, wwwww),
  KEY idx_cscscsc (data, nunm, ssw)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='cs';
    """

    tokens = mtp.mysql_token_parser(sql)
    print(tokens)
    assert isinstance(tokens, dict)

    hope_tablename = 'tab_name'
    assert hope_tablename == tokens['data']['data'][_c.TABLE_NAME]

    hope_engine = 'InnoDB'
    assert hope_engine == tokens['data']['data'][_c.TABLE_OPTION_ENGINE]

    hope_charset = 'utf8'
    assert hope_charset == tokens['data']['data'][_c.TABLE_OPTION_CHARSET]

    hope_column_len = 8
    assert hope_column_len == len(tokens['data']['data'][_c.CREATE_DEFINITIONS]['columns'])

    hope_common_index_len = 2
    assert hope_common_index_len == len(tokens['data']['data'][_c.CREATE_DEFINITIONS]['indexs'][_c.COMMON_KEY])

    hope_columnname = ["id", "uid", "name", "amount", "create_date", "create_time", "update_time", "okmysite"]
    for i in tokens['data']['data'][_c.CREATE_DEFINITIONS]['columns']:
        assert i[_c.COLUMN_NAME] in hope_columnname
