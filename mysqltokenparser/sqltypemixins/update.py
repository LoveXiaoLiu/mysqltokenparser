# coding: utf-8
import antlr4
from mysqltokenparser.utils import iterchild
from mysqltokenparser.MySqlParser import MySqlParser
from mysqltokenparser.constant import *


class UpdateMixin(object):
    """
    delete type:
        singleDeleteStatement multipleDeleteStatement
    """
    def enterUpdateStatement(self, ctx):
        data = {}
        self.ret['data'] = {
            'type': DML_TYPE_UPDATESTATEMENT,
            'data': data
        }

        children = ctx.children
        for child in children:
            if isinstance(child, MySqlParser.MultipleUpdateStatementContext):
                data.update(self._enterMultipleUpdateStatement(child))

            if isinstance(child, MySqlParser.SingleUpdateStatementContext):
                data.update(self._enterSingleUpdateStatement(child))

    @iterchild
    def _enterMultipleUpdateStatement(self, child, ret):
        pass

    @iterchild
    def _enterSingleUpdateStatement(self, child, ret):
        if isinstance(child, MySqlParser.TableNameContext):
            ret[TABLE_NAME] = self._get_last_name(child)

        if isinstance(child, MySqlParser.PredicateExpressionContext):
            ret.update(self._enterPredicateExpression(child))

        if isinstance(child, MySqlParser.UpdatedElementContext):
            update_elements = ret.setdefault('update_elements', [])
            update_elements.append(self._enterUpdatedElement(child).get('update_element'))

    @iterchild
    def _enterUpdatedElement(self, child, ret):
        update_element = ret.setdefault('update_element', [])
        if isinstance(child, MySqlParser.FullColumnNameContext):
            update_element.append(self._get_last_name(child))
        if isinstance(child, MySqlParser.PredicateExpressionContext):
            update_element.extend(self._enterPredicateExpression(child).get('where_expression'))
