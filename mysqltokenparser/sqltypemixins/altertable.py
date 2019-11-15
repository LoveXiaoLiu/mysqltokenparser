# coding: utf-8
import antlr4

from mysqltokenparser.utils import (
    iterchild, ALTER_TABLE, ADD_COLUMN, MODIFY_COLUMN, CHANGE_COLUMN, ADD_INDEX, DROP_COLUMN)
from mysqltokenparser.MySqlParser import MySqlParser


class AlterTableMixin:
    def enterAlterTable(self, ctx):
        data = {}
        self.ret['data'] = {
            'type': ALTER_TABLE,
            'data': data
        }
        alter_data = data.setdefault('alter_data', [])

        children = ctx.children
        for child in children:
            if isinstance(child, MySqlParser.TableNameContext):
                data['tablename'] = self._get_last_name(child)
            if isinstance(child, MySqlParser.AlterByAddColumnContext):
                alter_data.append({
                    "type": ADD_COLUMN,
                    "data": self._enterAlterByAddColumn(child)
                })
            if isinstance(child, MySqlParser.AlterByModifyColumnContext):
                alter_data.append({
                    "type": MODIFY_COLUMN,
                    "data": self._enterAlterByModifyColumn(child)
                })
            if isinstance(child, MySqlParser.AlterByChangeColumnContext):
                alter_data.append({
                    "type": CHANGE_COLUMN,
                    "data": self._enterAlterByChangeColumn(child)
                })
            if isinstance(child, MySqlParser.AlterByAddIndexContext):
                alter_data.append({
                    "type": ADD_INDEX,
                    "data": self._enterAlterByAddIndex(child)
                })
            if isinstance(child, MySqlParser.AlterByAddUniqueKeyContext):
                alter_data.append({
                    "type": ADD_INDEX,
                    "data": self._enterAlterByAddIndex(child)
                })
            if isinstance(child, MySqlParser.AlterByDropColumnContext):
                alter_data.append({
                    "type": DROP_COLUMN,
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
        if isinstance(child, MySqlParser.SimpleDataTypeContext):
            ret.update(self._enterSimpleDataType(child))

    @iterchild
    def _enterSimpleDataType(self, child, ret):
        ret.update({
            'column_types': self._get_last_name(child),
            'data': {}
        })

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
