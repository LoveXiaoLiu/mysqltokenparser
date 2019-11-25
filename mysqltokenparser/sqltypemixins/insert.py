# coding: utf-8
import antlr4
from mysqltokenparser.utils import iterchild
from mysqltokenparser.MySqlParser import MySqlParser
from mysqltokenparser.constant import *


class InsertMixin(object):
    """

    """
    def enterInsertStatement(self, ctx):
        data = {}
        self.ret['data'] = {
            'type': DML_TYPE_INSERTSTATEMENT,
            'data': data
        }

        children = ctx.children
        for child in children:
            if isinstance(child, MySqlParser.TableNameContext):
                data[TABLE_NAME] = self._get_last_name(child)

            if isinstance(child, MySqlParser.UidListContext):
                data.update(self._enterUidList(child))

            if isinstance(child, MySqlParser.InsertStatementValueContext):
                data.update(self._enterInsertStatementValue(child))

    @iterchild
    def _enterUidList(self, child, ret):
        column_name = ret.setdefault(COLUMN_NAME, [])
        if isinstance(child, MySqlParser.UidContext):
            column_name.append(self._get_last_name(child))

    @iterchild
    def _enterInsertStatementValue(self, child, ret):
        insert_values = ret.setdefault('insert_values', [])
        if isinstance(child, MySqlParser.ExpressionsWithDefaultsContext):
            insert_values.append(self._enterExpressionsWithDefaults(child).get('insert_value'))

    @iterchild
    def _enterExpressionsWithDefaults(self, child, ret):
        insert_value = ret.setdefault('insert_value', [])
        if isinstance(child, MySqlParser.ExpressionOrDefaultContext):
            insert_value.extend(self._enterExpressionAtomPredicate(child).get('where_expression'))
