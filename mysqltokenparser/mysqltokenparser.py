# -*- coding: utf-8 -*-

"""Main module."""

import antlr4
from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream
from antlr4.InputStream import InputStream

from MySqlLexer import MySqlLexer
from MySqlParser import MySqlParser
from MySqlParserListener import MySqlParserListener
from utils import iterchild


class MyListener(MySqlParserListener):
    def __init__(self, ret):
        self.ret = ret

    def enterDdlStatement(self, ctx):
        self.ret['type'] = 'ddl'

    def enterAlterTable(self, ctx):
        data = {}
        self.ret['data'] = {
            'type': 'altertable',
            'data': data
        }
        alter_data = data.setdefault('alter_data', [])

        children = ctx.children
        for child in children:
            if isinstance(child, MySqlParser.TableNameContext):
                data['tablename'] = self._get_last_name(child)
            if isinstance(child, MySqlParser.AlterByAddColumnContext):
                alter_data.append({
                    "type": 'addcolumn',
                    "data": self._enterAlterByAddColumn(child)
                })
            if isinstance(child, MySqlParser.AlterByModifyColumnContext):
                alter_data.append({
                    "type": 'modifycolumn',
                    "data": self._enterAlterByModifyColumn(child)
                })
            if isinstance(child, MySqlParser.AlterByChangeColumnContext):
                alter_data.append({
                    "type": 'modifycolumn',
                    "data": self._enterAlterByChangeColumn(child)
                })
            if isinstance(child, MySqlParser.AlterByAddIndexContext):
                alter_data.append({
                    "type": 'addindex',
                    "data": self._enterAlterByAddIndex(child)
                })
            if isinstance(child, MySqlParser.AlterByAddUniqueKeyContext):
                alter_data.append({
                    "type": 'addindex',
                    "data": self._enterAlterByAddIndex(child)
                })
            if isinstance(child, MySqlParser.AlterByDropColumnContext):
                alter_data.append({
                    "type": 'dropcolumn',
                    "data": self._enterAlterByDropColumn(child)
                })

    @iterchild
    def _enterAlterByDropColumn(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            ret['columnname'] = self._get_last_name(child)

    @iterchild
    def _enterAlterByAddIndex(self, child, ret):
        columnnames = []
        if isinstance(child, MySqlParser.UidContext):
            ret['indexname'] = self._get_last_name(child)
        if isinstance(child, MySqlParser.IndexColumnNamesContext):
            columnnames = self._enterIndexColumnNames(child).get('columns', [])

        ret['indexdefinition'] = {
            'columnnames': columnnames
        }

    @iterchild
    def _enterIndexColumnNames(self, child, ret):
        if isinstance(child, MySqlParser.IndexColumnNameContext):
            columns = ret.setdefault('columns', [])
            columns.append(self._get_last_name(child))

    @iterchild
    def _enterAlterByChangeColumn(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            if ret.get('columnname'):
                ret['new_columnname'] = self._get_last_name(child)
            else:
                ret['columnname'] = self._get_last_name(child)
        if isinstance(child, MySqlParser.ColumnDefinitionContext):
            ret['columndefinition'] = self._enterColumnDefinition(child)

    @iterchild
    def _enterAlterByModifyColumn(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            ret['columnname'] = self._get_last_name(child)
        if isinstance(child, MySqlParser.ColumnDefinitionContext):
            ret['columndefinition'] = self._enterColumnDefinition(child)

    @iterchild
    def _enterAlterByAddColumn(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            ret['columnname'] = self._get_last_name(child)
        if isinstance(child, MySqlParser.ColumnDefinitionContext):
            ret['columndefinition'] = self._enterColumnDefinition(child)

    @iterchild
    def _enterColumnDefinition(self, child, ret):
        if isinstance(child, MySqlParser.StringDataTypeContext):
            ret.update(self._enterStringDataType(child))
        if isinstance(child, MySqlParser.DimensionDataTypeContext):
            ret.update(self._enterDimensionDataType(child))

    @iterchild
    def _enterDimensionDataType(self, child, ret):
        ret.update({
            'column_types': self._get_last_name(child),
            'data': {}
        })

    @iterchild
    def _enterStringDataType(self, child, ret):
        if isinstance(child, antlr4.tree.Tree.TerminalNodeImpl):
            ret['column_type'] = self._get_last_name(child)
        if isinstance(child, MySqlParser.LengthOneDimensionContext):
            ret['data'] = self._enterLengthOneDimension(child)

    @iterchild
    def _enterLengthOneDimension(self, child, ret):
        if isinstance(child, MySqlParser.DecimalLiteralContext):
            ret['decimalliteral'] = self._get_last_name(child)

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
