#!/usr/bin/env python
# coding:utf-8

import pytest
from helper import mysqltokenparser as mtp
from helper import constant as _c


def test_simpleselect():
    sql = u"""
    select id as qq, name as ww, age as ee, class as rr
    from student as s, teacher as t
    where name='cs' and age=26;
    """

    tokens = mtp.mysql_token_parser(sql)
    print(tokens)
    assert isinstance(tokens, dict)
