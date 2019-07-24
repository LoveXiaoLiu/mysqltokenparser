#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mysqltokenparser` package."""

import pytest


from helper import mysqltokenparser as mtp


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
      `id` bigint(20) NOT NULL COMMENT '主键id',
      `operation_seq` varchar(30) NOT NULL COMMENT '运营活动序列号',
      `award_user_id` bigint(20) NOT NULL COMMENT '中奖用户id',
      `award_type` int(11) DEFAULT NULL COMMENT '中奖奖品类型',
      `award_id` varchar(40) DEFAULT NULL UNIQUE KEY COMMENT '中奖奖品编号',
      `award_content` varchar(20)  DEFAULT NULL COMMENT '中奖内容',
      `award_reason` varchar(30)  DEFAULT NULL,
      `award_source` int(11) DEFAULT NULL COMMENT '中奖来源',
      `state` tinyint(4) NOT NULL PRIMARY KEY COMMENT '状态',
      `addtime` datetime NOT NULL COMMENT '新建时间',
      `updatetime` datetime NOT NULL COMMENT '更新时间',
      `ip` varchar(50)  DEFAULT NULL COMMENT '中奖者ip',
      `imei` varchar(50)  DEFAULT NULL COMMENT '中奖者设备号',
      `intext` int(11) DEFAULT NULL COMMENT '备用字段',
      `longext` bigint(20) DEFAULT NULL COMMENT '备用字段',
      `strext` varchar(200)  DEFAULT NULL COMMENT '备用字段',
      PRIMARY KEY (id),
      UNIQUE KEY `idx_op_seq_uid_type` (`operation_seq`,`award_user_id`,`award_type`),
      KEY `idx_op_uid_type` (`award_user_id`,`award_type`),
      KEY `idx_op_uid_sss` (longext(10))
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='招才猫幸运值系列活动中奖记录表';
    """

    token_obj = mtp.mysql_token_parser(sql)
    tokens = token_obj.get_tokens()
    assert isinstance(tokens, dict)
