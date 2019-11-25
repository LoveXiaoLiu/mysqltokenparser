# -*- coding: utf-8 -*-

"""Main module."""

from antlr4.InputStream import InputStream
from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream

from MySqlLexer import MySqlLexer
from MySqlParser import MySqlParser
from MySqlParserListener import MySqlParserListener
from sqltypemixins import (
    AlterTableMixin, CreateTableMixin, SelectMixin, InsertMixin, DeleteMixin, UpdateMixin
)
from constant import *


class MyListener(
    AlterTableMixin, CreateTableMixin, SelectMixin, InsertMixin,
    DeleteMixin, UpdateMixin, MySqlParserListener
):
    def __init__(self, ret):
        self.ret = ret

    def enterDdlStatement(self, ctx):
        self.ret['type'] = SQL_TYPE_DDL

    def enterDmlStatement(self, ctx):
        self.ret['type'] = SQL_TYPE_DML

    @staticmethod
    def _get_last_name(ctx):
        while hasattr(ctx, 'children'):
            ctx = ctx.children[0]

        return ctx.symbol.text


class CaseChangingCharInputStream(InputStream):
    def __init__(self, data, upper=True):
        super(CaseChangingCharInputStream, self).__init__(data)
        self.upper = upper

    def LA(self, pos):
        value = super(CaseChangingCharInputStream, self).LA(pos)
        if 0 <= value < 256:
            if pos <= 0: return value
            str_value = chr(value)
            return ord(str_value.upper()) if self.upper else ord(str_value.lower())
        else:
            return value


class CaseChangingCharFileStream(FileStream, CaseChangingCharInputStream):
    def __init__(self, file, upper=True):
        super(CaseChangingCharFileStream, self).__init__(file)
        self.upper = upper


class SqlParseHandle(object):
    def __init__(self, sql):
        self._tokens = {}
        self.sql = sql
        self.input_stream = CaseChangingCharInputStream(self.sql)
        self.lexer = MySqlLexer(self.input_stream)
        self.token_stream = CommonTokenStream(self.lexer)
        self.parser = MySqlParser(self.token_stream)
        self.tree = self.parser.root()
        self.printer = MyListener(self._tokens)
        self.walker = ParseTreeWalker()

    def get_tokens(self):
        self.walker.walk(self.printer, self.tree)
        return self._tokens


def mysql_token_parser(sql):
    return SqlParseHandle(sql).get_tokens()


if __name__ == "__main__":
    print mysql_token_parser(u"""""")
