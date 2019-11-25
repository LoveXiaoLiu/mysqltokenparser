#!/usr/bin/env python
# coding:utf-8

import pytest
from helper import mysqltokenparser as mtp
from helper import constant as _c


def test_simpleselect():
    sql = u"""
    UPDATE table_name SET field1='new-value1', field2='new-value2' WHERE id=23 and name="css";
    """

    tokens = mtp.mysql_token_parser(sql)
    print(tokens)
    assert isinstance(tokens, dict)
