# coding: utf-8
from mysqltokenparser.utils import iterchild
from mysqltokenparser.MySqlParser import MySqlParser
from mysqltokenparser.constant import *


class SelectMixin:
    """
    select type:
        simpleSelect parenthesisSelect unionSelect unionParenthesisSelect
    """
    def enterSimpleSelect(self, ctx):
        data = {}
        self.ret['data'] = {
            'type': DML_TYPE_SELECTSTATEMENT,
            'data': {
                'type': SELECT_TYPE_SIMPLESELECT,
                'data': data
            }
        }

        children = ctx.children
        for child in children:
            if isinstance(child, MySqlParser.QuerySpecificationContext):
                data.update(self._enterQuerySpecification(child))

    @iterchild
    def _enterQuerySpecification(self, child, ret):
        if isinstance(child, MySqlParser.SelectElementsContext):
            ret.update(self._enterSelectElements(child))

        if isinstance(child, MySqlParser.FromClauseContext):
            ret['from_clause'] = self._enterFromClause(child)

    @iterchild
    def _enterFromClause(self, child, ret):
        if isinstance(child, MySqlParser.TableSourcesContext):
            ret.update(self._enterTableSources(child))

        if isinstance(child, MySqlParser.LogicalExpressionContext):
            ret.update(self._enterLogicalExpression(child))

    @iterchild
    def _enterLogicalExpression(self, child, ret):
        pass

    @iterchild
    def _enterTableSources(self, child, ret):
        select_table = ret.setdefault('from_tables', [])
        if isinstance(child, MySqlParser.TableSourceBaseContext):
            select_table.append(self._enterTableSourceBase(child))

    @iterchild
    def _enterTableSourceBase(self, child, ret):
        if isinstance(child, MySqlParser.AtomTableItemContext):
            ret.update(self._enterAtomTableItem(child))

    @iterchild
    def _enterAtomTableItem(self, child, ret):
        if isinstance(child, MySqlParser.TableNameContext):
            ret[TABLE_NAME] = self._get_last_name(child)
        if isinstance(child, MySqlParser.UidContext):
            ret['as'] = self._get_last_name(child)

    @iterchild
    def _enterSelectElements(self, child, ret):
        select_element = ret.setdefault('select_element', [])
        if isinstance(child, MySqlParser.SelectColumnElementContext):
            select_element.append(self._enterSelectColumnElement(child))

    @iterchild
    def _enterSelectColumnElement(self, child, ret):
        if isinstance(child, MySqlParser.FullColumnNameContext):
            ret[COLUMN_NAME] = self._get_last_name(child)
        if isinstance(child, MySqlParser.UidContext):
            ret['as'] = self._get_last_name(child)
