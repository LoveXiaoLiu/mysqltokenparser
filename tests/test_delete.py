#!/usr/bin/env python
# coding:utf-8

import pytest
from helper import mysqltokenparser as mtp
from helper import constant as _c


def test_simpleselect():
    sql = u"""
    delete a, b from student a, teacher b where a.id=b.name and b.age = 32;
    """

    tokens = mtp.mysql_token_parser(sql)
    print(tokens)
    assert isinstance(tokens, dict)
