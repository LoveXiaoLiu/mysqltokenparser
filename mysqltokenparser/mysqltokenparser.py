# -*- coding: utf-8 -*-

"""Main module."""

from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream
from antlr4.InputStream import InputStream

from MySqlLexer import MySqlLexer
from MySqlParser import MySqlParser
from MySqlParserListener import MySqlParserListener


class TABLE_ATTR_MAP(object):
    tablename = 'tablenames'
    indexname = 'indexnames'
    alluid = 'alluids'
    columnnames = 'columnnames'


class MyListener(MySqlParserListener):
    def __init__(self, handle):
        self.w_handle = handle

    def _set_data(self, name, value):
        self.w_handle.set_tokens(name, value)

    def enterDdlStatement(self, ctx):
        # print ctx
        pass

    # table name
    def enterTableName(self, ctx):
        value = ctx.getText()
        self._set_data(TABLE_ATTR_MAP.tablename, value)
        # self.w_handle.set_interface(TABLE_ATTR_MAP.tablename, value)

    # table index Column Names
    def enterIndexColumnNames(self, ctx):
        value = ctx.getText()
        self._set_data(TABLE_ATTR_MAP.indexname, value)
        # self.w_handle.set_interface(TABLE_ATTR_MAP.indexname, value)

    # statement uid
    def enterUid(self, ctx):
        value = ctx.getText()
        # self.set_data(TABLE_ATTR_MAP.alluid, value)
        # self.w_handle.set_interface(TABLE_ATTR_MAP.alluid, value)

        if not (isinstance(ctx.parentCtx, (
            MySqlParser.UniqueKeyTableConstraintContext,
            MySqlParser.ForeignKeyTableConstraintContext,
            MySqlParser.SimpleIndexDeclarationContext,
            MySqlParser.SpecialIndexDeclarationContext,
            MySqlParser.IndexColumnNameContext,
        )) or isinstance(ctx.parentCtx.parentCtx, MySqlParser.TableNameContext)):
            self._set_data(TABLE_ATTR_MAP.columnnames, value)
            # self.w_handle.set_interface(TABLE_ATTR_MAP.columnnames, value)

    # PrimaryKey Column
    def enterPrimaryKeyColumnConstraint(self, ctx):
        if isinstance(ctx.parentCtx.parentCtx, MySqlParser.ColumnDeclarationContext):
            value = ctx.parentCtx.parentCtx.children[0].getText()
            # self.w_handle.set_interface(TABLE_ATTR_MAP.indexname, "({0})".format(value))
            self._set_data(TABLE_ATTR_MAP.indexname, "({0})".format(value))

    # UniqueKey Column
    def enterUniqueKeyColumnConstraint(self, ctx):
        if isinstance(ctx.parentCtx.parentCtx, MySqlParser.ColumnDeclarationContext):
            value = ctx.parentCtx.parentCtx.children[0].getText()
            # self.w_handle.set_interface(TABLE_ATTR_MAP.indexname, "({0})".format(value))
            self._set_data(TABLE_ATTR_MAP.indexname, "({0})".format(value))


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


if __name__ == '__main__':


    alter_sql1 = u"ALTER TABLE t_a_gun2_6_dw_pfm_emp_cm ADD INDEX idx_eob_date(empid_org_bus (200),pfm_date);"
    alter_sql2 = u"ALTER TABLE tab_name ADD address  varchar(100) NOT NULL DEFAULT '' COMMENT '地址' AFTER  amount;"
    alter_sql3 = u"ALTER TABLE tab_name ADD address01  varchar(100) NOT NULL DEFAULT '' COMMENT '地址1' , ADD address02  varchar(100) NOT NULL DEFAULT '' COMMENT '地址2' ;"

    #### debug code
    sql = alter_sql1
    a = mysql_token_parser(sql)
    e = a.get_tokens()
    print "tokens", e
