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

    sql2 = """
    select * from teacher where age<=26 and (sex="man" or age >26) and sex="women";
    """

    tokens = mtp.mysql_token_parser(sql2)
    assert isinstance(tokens, dict)
