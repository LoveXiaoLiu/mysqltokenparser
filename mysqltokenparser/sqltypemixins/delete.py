# coding: utf-8
import antlr4
from mysqltokenparser.utils import iterchild
from mysqltokenparser.MySqlParser import MySqlParser
from mysqltokenparser.constant import *


class DeleteMixin(object):
    """
    delete type:
        singleDeleteStatement multipleDeleteStatement
    """
    def enterDeleteStatement(self, ctx):
        data = {}
        self.ret['data'] = {
            'type': DML_TYPE_DELETESTATEMENT,
            'data': data
        }

        children = ctx.children
        for child in children:
            if isinstance(child, MySqlParser.MultipleDeleteStatementContext):
                data.update(self._enterMultipleDeleteStatement(child))

            if isinstance(child, MySqlParser.SingleDeleteStatementContext):
                data.update(self._enterSingleDeleteStatement(child))

    @iterchild
    def _enterMultipleDeleteStatement(self, child, ret):
        table_names = ret.setdefault('table_names', [])
        if isinstance(child, MySqlParser.TableNameContext):
            table_names.append(self._get_last_name(child))

        if isinstance(child, MySqlParser.LogicalExpressionContext):
            ret.update(self._enterLogicalExpression(child))

        if isinstance(child, MySqlParser.TableSourcesContext):
            ret.update(self._enterTableSources(child))

    @iterchild
    def _enterSingleDeleteStatement(self, child, ret):
        if isinstance(child, MySqlParser.TableNameContext):
            ret[TABLE_NAME] = self._get_last_name(child)

        if isinstance(child, MySqlParser.PredicateExpressionContext):
            ret.update(self._enterPredicateExpression(child))
