# coding: utf-8
import antlr4

from mysqltokenparser.utils import iterchild
from mysqltokenparser.MySqlParser import MySqlParser
from mysqltokenparser.constant import *


class AlterTableMixin(object):
    def enterAlterTable(self, ctx):
        data = {}
        self.ret['data'] = {
            'type': DDL_TYPE_ALTERTABLE,
            'data': data
        }
        alter_data = data.setdefault('alter_data', [])

        children = ctx.children
        for child in children:
            if isinstance(child, MySqlParser.TableNameContext):
                data[TABLE_NAME] = self._get_last_name(child)
            if isinstance(child, MySqlParser.AlterByAddColumnContext):
                alter_data.append({
                    "type": ALTER_TABLE_TYPE_ADDCOLUMN,
                    "data": self._enterAlterByAddColumn(child)
                })
            if isinstance(child, MySqlParser.AlterByModifyColumnContext):
                alter_data.append({
                    "type": ALTER_TABLE_TYPE_MODIFYCOLUMN,
                    "data": self._enterAlterByModifyColumn(child)
                })
            if isinstance(child, MySqlParser.AlterByChangeColumnContext):
                alter_data.append({
                    "type": ALTER_TABLE_TYPE_CHANGECOLUMN,
                    "data": self._enterAlterByChangeColumn(child)
                })
            if isinstance(child, MySqlParser.AlterByAddIndexContext):
                alter_data.append({
                    "type": ALTER_TABLE_TYPE_ADDINDEX,
                    "data": self._enterAlterByAddIndex(child)
                })
            if isinstance(child, MySqlParser.AlterByAddPrimaryKeyContext):
                alter_data.append({
                    "type": ALTER_TABLE_TYPE_ADDPRIMARYKEY,
                    "data": self._enterAlterByAddIndex(child)
                })
            if isinstance(child, MySqlParser.AlterByAddUniqueKeyContext):
                alter_data.append({
                    "type": ALTER_TABLE_TYPE_ADDUNIQUEKEY,
                    "data": self._enterAlterByAddIndex(child)
                })
            if isinstance(child, MySqlParser.AlterByDropColumnContext):
                alter_data.append({
                    "type": ALTER_TABLE_TYPE_DROPCOLUMN,
                    "data": self._enterAlterByDropColumn(child)
                })
            if isinstance(child, MySqlParser.AlterByDropIndexContext):
                alter_data.append({
                    "type": ALTER_TABLE_TYPE_DROPINDEX,
                    "data": self._enterAlterByDropIndex(child)
                })
            if isinstance(child, MySqlParser.AlterByDropPrimaryKeyContext):
                alter_data.append({
                    "type": ALTER_TABLE_TYPE_DROPPRIMARYKEY,
                    "data": {}
                })

    @iterchild
    def _enterAlterByDropIndex(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            ret[INDEX_NAME] = self._get_last_name(child)

    @iterchild
    def _enterAlterByDropColumn(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            ret[COLUMN_NAME] = self._get_last_name(child)

    @iterchild
    def _enterAlterByAddIndex(self, child, ret):
        columnnames = []
        if isinstance(child, MySqlParser.UidContext):
            ret[INDEX_NAME] = self._get_last_name(child)
        if isinstance(child, MySqlParser.IndexColumnNamesContext):
            columnnames = self._enterIndexColumnNames(child).get('columns', [])

        ret[INDEX_DEFINITION] = {
            'columns': columnnames
        }

    @iterchild
    def _enterIndexColumnNames(self, child, ret):
        if isinstance(child, MySqlParser.IndexColumnNameContext):
            columns = ret.setdefault('columns', [])
            columns.append(self._get_last_name(child))

    @iterchild
    def _enterAlterByChangeColumn(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            if ret.get(COLUMN_NAME):
                ret['new_column_name'] = self._get_last_name(child)
            else:
                ret[COLUMN_NAME] = self._get_last_name(child)
        if isinstance(child, MySqlParser.ColumnDefinitionContext):
            ret[COLUMN_DEFINITION] = self._enterColumnDefinition(child)

    @iterchild
    def _enterAlterByModifyColumn(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            ret[COLUMN_NAME] = self._get_last_name(child)
        if isinstance(child, MySqlParser.ColumnDefinitionContext):
            ret[COLUMN_DEFINITION] = self._enterColumnDefinition(child)

    @iterchild
    def _enterAlterByAddColumn(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            ret[COLUMN_NAME] = self._get_last_name(child)
        if isinstance(child, MySqlParser.ColumnDefinitionContext):
            ret[COLUMN_DEFINITION] = self._enterColumnDefinition(child)

    @iterchild
    def _enterColumnDefinition(self, child, ret):
        if isinstance(child, MySqlParser.StringDataTypeContext):
            ret.update(self._enterStringDataType(child))
        if isinstance(child, MySqlParser.DimensionDataTypeContext):
            ret.update(self._enterDimensionDataType(child))
        if isinstance(child, MySqlParser.SimpleDataTypeContext):
            ret.update(self._enterSimpleDataType(child))

        if isinstance(child, MySqlParser.NullColumnConstraintContext):
            ret.update(self._enterNullColumnConstraint(child))
        if isinstance(child, MySqlParser.AutoIncrementColumnConstraintContext):
            ret.update(self._enterAutoIncrementColumnConstraint(child))
        if isinstance(child, MySqlParser.CommentColumnConstraintContext):
            ret.update(self._enterCommentColumnConstraint(child))
        if isinstance(child, MySqlParser.PrimaryKeyColumnConstraintContext):
            ret.update(self._enterPrimaryKeyColumnConstraint(child))
        if isinstance(child, MySqlParser.DefaultColumnConstraintContext):
            ret.update(self._enterDefaultColumnConstraint(child))

    @iterchild
    def _enterDefaultColumnConstraint(self, child, ret):
        if isinstance(child, MySqlParser.DefaultValueContext):
            ret['default'] = self._get_last_name(child)

    def _enterPrimaryKeyColumnConstraint(self, ctx):
        return {
            PRIMARY_KEY: True
        }

    def _enterCommentColumnConstraint(self, ctx):
        return {
            'comment': self._get_last_name(ctx.children[1])
        }

    def _enterAutoIncrementColumnConstraint(self, ctx):
        return {
            'auto_increment': True
        }

    @iterchild
    def _enterNullColumnConstraint(self, child, ret):
        if isinstance(child, MySqlParser.NullNotnullContext):
            ret['null'] = False

    @iterchild
    def _enterSimpleDataType(self, child, ret):
        ret.update({
            COLUMN_TYPE: self._get_last_name(child),
            COLUMN_TYPE_DATA: {}
        })

    @iterchild
    def _enterDimensionDataType(self, child, ret):
        if isinstance(child, antlr4.tree.Tree.TerminalNodeImpl):
            ret[COLUMN_TYPE] = self._get_last_name(child)
        if isinstance(child, MySqlParser.LengthOneDimensionContext):
            ret[COLUMN_TYPE_DATA] = self._enterLengthOneDimension(child)
        if isinstance(child, MySqlParser.LengthTwoDimensionContext):
            ret[COLUMN_TYPE_DATA] = self._enterLengthTwoDimension(child)
        if isinstance(child, MySqlParser.LengthTwoOptionalDimensionContext):
            ret[COLUMN_TYPE_DATA] = self._enterLengthTwoDimension(child)

    @iterchild
    def _enterStringDataType(self, child, ret):
        if isinstance(child, antlr4.tree.Tree.TerminalNodeImpl):
            ret[COLUMN_TYPE] = self._get_last_name(child)
        if isinstance(child, MySqlParser.LengthOneDimensionContext):
            ret[COLUMN_TYPE_DATA] = self._enterLengthOneDimension(child)

    @iterchild
    def _enterLengthTwoDimension(self, child, ret):
        if isinstance(child, MySqlParser.DecimalLiteralContext):
            decimal_literal = ret.setdefault('decimal_literal', [])
            decimal_literal.append(self._get_last_name(child))

    @iterchild
    def _enterLengthOneDimension(self, child, ret):
        if isinstance(child, MySqlParser.DecimalLiteralContext):
            decimal_literal = ret.setdefault('decimal_literal', [])
            decimal_literal.append(self._get_last_name(child))
