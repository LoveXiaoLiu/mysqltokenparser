# coding: utf-8
import antlr4
from mysqltokenparser.utils import iterchild
from mysqltokenparser.MySqlParser import MySqlParser
from mysqltokenparser.constant import *


class SelectMixin(object):
    """
    select type:
        simpleSelect parenthesisSelect unionSelect unionParenthesisSelect

    just support simpleSelect type
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
        where_expression = ret.setdefault('where_expression', [])
        if isinstance(child, MySqlParser.LogicalExpressionContext):
            where_expression.append(self._enterLogicalExpression(child).get('where_expression'))

        if isinstance(child, MySqlParser.LogicalOperatorContext):
            where_expression.append(self._get_last_name(child))

        if isinstance(child, MySqlParser.PredicateExpressionContext):
            where_expression.append(self._enterPredicateExpression(child).get('where_expression'))

    @iterchild
    def _enterPredicateExpression(self, child, ret):
        where_expression = ret.setdefault('where_expression', [])
        if isinstance(child, MySqlParser.BinaryComparasionPredicateContext):
            where_expression.extend(self._enterBinaryComparasionPredicate(child).get('where_expression'))

        if isinstance(child, MySqlParser.ExpressionAtomPredicateContext):
            where_expression.extend(self._enterExpressionAtomPredicate(child).get('where_expression'))

    @iterchild
    def _enterExpressionAtomPredicateForFullColumnNameExpressionAtomContext(self, child, ret):
        full_columns = ret.setdefault('full_columns', [])
        if isinstance(child, MySqlParser.FullColumnNameExpressionAtomContext):
            full_columns.append(''.join(self._enterFullColumnName(child).get('full_column')))
        if isinstance(child, MySqlParser.ConstantExpressionAtomContext):
            full_columns.append(self._enterConstantExpressionAtom(child).get('constant_expression'))

    @iterchild
    def _enterFullColumnName(self, child, ret):
        if isinstance(child, MySqlParser.FullColumnNameContext):
            ret.update(self._enterFullColumnNameDetail(child))

    @iterchild
    def _enterFullColumnNameDetail(self, child, ret):
        full_column = ret.setdefault('full_column', [])
        if isinstance(child, MySqlParser.UidContext) or\
            isinstance(child, MySqlParser.DottedIdContext):
            full_column.append(self._get_last_name(child))

    @iterchild
    def _enterExpressionAtomPredicate(self, child, ret):
        where_expression = ret.setdefault('where_expression', [])
        if isinstance(child, MySqlParser.NestedExpressionAtomContext):
            where_expression.extend(self._enterNestedExpressionAtom(child).get('where_expression'))

        if isinstance(child, MySqlParser.PredicateExpressionContext):
            where_expression.extend(self._enterPredicateExpression(child).get('where_expression'))

        if isinstance(child, MySqlParser.ConstantExpressionAtomContext):
            where_expression.append(self._enterConstantExpressionAtom(child).get('constant_expression'))

    @iterchild
    def _enterConstantExpressionAtom(self, child, ret):
        if isinstance(child, MySqlParser.ConstantContext):
            ret['constant_expression'] = self._get_last_name(child)

    @iterchild
    def _enterNestedExpressionAtom(self, child, ret):
        if isinstance(child, MySqlParser.LogicalExpressionContext):
            ret.update(self._enterLogicalExpression(child))

    @iterchild
    def _enterBinaryComparasionPredicate(self, child, ret):
        where_expression = ret.setdefault('where_expression', [])
        if isinstance(child, MySqlParser.ExpressionAtomPredicateContext):
            where_expression.extend(
                self._enterExpressionAtomPredicateForFullColumnNameExpressionAtomContext(
                    child
                ).get('full_columns', [])
            )

        if isinstance(child, MySqlParser.ComparisonOperatorContext):
            where_expression.append(''.join(self._enterComparisonOperator(child).get('comparison_oper')))

    @iterchild
    def _enterComparisonOperator(self, child, ret):
        comparison_oper = ret.setdefault('comparison_oper', [])
        comparison_oper.append(self._get_last_name(child))

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
        if isinstance(child, antlr4.tree.Tree.TerminalNodeImpl):
            select_element.append({
                COLUMN_NAME: self._get_last_name(child)
            })

    @iterchild
    def _enterSelectColumnElement(self, child, ret):
        if isinstance(child, MySqlParser.FullColumnNameContext):
            ret[COLUMN_NAME] = self._get_last_name(child)
        if isinstance(child, MySqlParser.UidContext):
            ret['as'] = self._get_last_name(child)
