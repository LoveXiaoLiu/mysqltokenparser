# -*- coding: utf-8 -*-

"""Top-level package for mysqltokenparser."""

__author__ = """gra55"""
__email__ = 'shuai.grass@gmail.com'
__version__ = '2.2.0'


from .mysqltokenparser import mysql_token_parser
import constant

__all__ = ['mysql_token_parser', 'constant']
