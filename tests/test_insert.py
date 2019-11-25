#!/usr/bin/env python
# coding:utf-8

import pytest
from helper import mysqltokenparser as mtp
from helper import constant as _c


def test_simpleselect():
    sql = u"""
    insert into teacher (age, sex) values (25, 'women'), (30, 'women');
    """

    tokens = mtp.mysql_token_parser(sql)
    print(tokens)
    assert isinstance(tokens, dict)
