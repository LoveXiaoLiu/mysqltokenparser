# -*- coding: utf-8 -*-

"""Main module."""

from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream
from antlr4.InputStream import InputStream

from MySqlLexer import MySqlLexer
from MySqlParser import MySqlParser
from MySqlParserListener import MySqlParserListener


class TABLE_ATTR_MAP:
    tablename = 'tablenames'
    indexname = 'indexnames'
    alluid = 'alluids'
    columnnames = 'columnnames'
    sqltype = 'sqltype'
    primarykey = "primarykey"
    uniquekey = "uniquekey"


class SQL_TYPE:
    DDL = 'ddl'
    DML = 'dml'
    DCL = 'dcl'


class MyListener(MySqlParserListener):
    def __init__(self, handle):
        self.w_handle = handle

    def _set_data(self, name, value):
        self.w_handle.set_tokens(name, value)

    def enterDdlStatement(self, ctx):
        self._set_data(TABLE_ATTR_MAP.sqltype, SQL_TYPE.DDL)

    def enterDmlStatement(self, ctx):
        self._set_data(TABLE_ATTR_MAP.sqltype, SQL_TYPE.DML)

    def enterAdministrationStatement(self, ctx):
        self._set_data(TABLE_ATTR_MAP.sqltype, SQL_TYPE.DCL)

    # table name
    def enterTableName(self, ctx):
        value = ctx.getText()
        self._set_data(TABLE_ATTR_MAP.tablename, value)

    # table index Column Names
    def enterIndexColumnNames(self, ctx):
        value = ctx.getText()
        self._set_data(TABLE_ATTR_MAP.indexname, value)

    # statement uid
    def enterUid(self, ctx):
        value = ctx.getText()
        # self.set_data(TABLE_ATTR_MAP.alluid, value)

        if not (isinstance(ctx.parentCtx, (
            MySqlParser.UniqueKeyTableConstraintContext,
            MySqlParser.ForeignKeyTableConstraintContext,
            MySqlParser.SimpleIndexDeclarationContext,
            MySqlParser.SpecialIndexDeclarationContext,
            MySqlParser.IndexColumnNameContext,
        )) or isinstance(ctx.parentCtx.parentCtx, MySqlParser.TableNameContext)):
            self._set_data(TABLE_ATTR_MAP.columnnames, value)

    # PrimaryKey Column
    def enterPrimaryKeyColumnConstraint(self, ctx):
        if isinstance(ctx.parentCtx.parentCtx, MySqlParser.ColumnDeclarationContext):
            value = ctx.parentCtx.parentCtx.children[0].getText()
            self._set_data(TABLE_ATTR_MAP.primarykey, "({0})".format(value))

    # UniqueKey Column
    def enterUniqueKeyColumnConstraint(self, ctx):
        if isinstance(ctx.parentCtx.parentCtx, MySqlParser.ColumnDeclarationContext):
            value = ctx.parentCtx.parentCtx.children[0].getText()
            self._set_data(TABLE_ATTR_MAP.uniquekey, "({0})".format(value))


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
        self.printer = MyListener(self)
        self.walker = ParseTreeWalker()
        self.walker.walk(self.printer, self.tree)

    def get_tokens(self):
        return self._tokens

    def set_tokens(self, name, value):
        value = value.replace('`', '')
        if value.startswith("("): value = value[1:]
        if value.endswith(")"): value = value[:-1]
        self._tokens.setdefault(name, []).append(value)


def mysql_token_parser(sql):
    return SqlParseHandle(sql)
