# -*- coding: utf-8 -*-

"""Main module."""

from antlr4.InputStream import InputStream
from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream

from MySqlLexer import MySqlLexer
from MySqlParser import MySqlParser
from MySqlParserListener import MySqlParserListener
from sqltypemixins.altertable import AlterTableMixin
from sqltypemixins.createtable import CreateTableMixin
from constant import SQL_TYPE_DDL


class MyListener(AlterTableMixin, CreateTableMixin, MySqlParserListener):
    def __init__(self, ret):
        self.ret = ret

    def enterDdlStatement(self, ctx):
        self.ret['type'] = SQL_TYPE_DDL

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
    print mysql_token_parser(u"""CREATE TABLE tab_name (
  id     		int         NOT NULL AUTO_INCREMENT COMMENT '主键',
  uid 			int         NOT NULL COMMENT '唯一流水id',
  name			varchar(20) NOT NULL DEFAULT '' COMMENT '名称',
  amount 		int         NOT NULL DEFAULT 0 COMMENT '数量',
  create_date	date        NOT NULL DEFAULT '1000-01-01' COMMENT '创建日期',
  create_time	datetime    DEFAULT '1000-01-01 00:00:00' COMMENT '创建时间',
  update_time 	timestamp   default current_timestamp on update current_timestamp COMMENT '更新时间(会自动更新，不需要刻意程序更新)',
  PRIMARY KEY (id),
  UNIQUE KEY uniq_uid (uid, ccccc),
  KEY idx_name (name, wwwww),
  KEY idx_cscscsc (data, nunm, ssw)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='测试表';""")
