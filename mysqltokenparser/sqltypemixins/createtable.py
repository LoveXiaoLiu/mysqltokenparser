# coding: utf-8
from mysqltokenparser.utils import iterchild
from mysqltokenparser.MySqlParser import MySqlParser
from mysqltokenparser.constant import *


class CreateTableMixin(object):
    """
    create table type: copyCreateTable queryCreateTable columnCreateTable

    just support columnCreateTable.
    """
    def enterColumnCreateTable(self, ctx):
        data = {}
        self.ret['data'] = {
            'type': DDL_TYPE_CREATETABLE,
            'data': data
        }

        children = ctx.children
        for child in children:
            if isinstance(child, MySqlParser.TableNameContext):
                data[TABLE_NAME] = self._get_last_name(child)

            if isinstance(child, MySqlParser.CreateDefinitionsContext):
                data[CREATE_DEFINITIONS] = self._enterCreateDefinitions(child)

            if isinstance(child, MySqlParser.TableOptionEngineContext):
                data[TABLE_OPTION_ENGINE] = self._enterTableOptionEngine(
                    child).get(TABLE_OPTION_ENGINE)

            if isinstance(child, MySqlParser.TableOptionCharsetContext):
                data[TABLE_OPTION_CHARSET] = self._enterTableOptionCharset(
                    child).get(TABLE_OPTION_CHARSET)

            if isinstance(child, MySqlParser.TableOptionCommentContext):
                data[TABLE_OPTION_COMMENT] = self._enterTableOptionComment(child)

    def _enterTableOptionComment(self, ctx):
        try:
            return self._get_last_name(ctx.children[2])
        except Exception as e:
            return ''

    @iterchild
    def _enterTableOptionCharset(self, child, ret):
        if isinstance(child, MySqlParser.CharsetNameContext):
            ret[TABLE_OPTION_CHARSET] = self._get_last_name(child)

    @iterchild
    def _enterTableOptionEngine(self, child, ret):
        if isinstance(child, MySqlParser.EngineNameContext):
            ret[TABLE_OPTION_ENGINE] = self._get_last_name(child)

    @iterchild
    def _enterCreateDefinitions(self, child, ret):
        if isinstance(child, MySqlParser.ColumnDeclarationContext):
            columns = ret.setdefault('columns', [])
            columns.append(self._enterColumnDeclaration(child))

        if isinstance(child, MySqlParser.ConstraintDeclarationContext):
            indexs = ret.setdefault('indexs', {})
            indexs.update(self._enterConstraintDeclaration(child))

        if isinstance(child, MySqlParser.IndexDeclarationContext):
            indexs = ret.setdefault('indexs', {})
            indexs.setdefault(COMMON_KEY, []).append(self._enterIndexDeclaration(child))

    @iterchild
    def _enterIndexDeclaration(self, child, ret):
        # common_key = ret.setdefault('common_key', [])
        if isinstance(child, MySqlParser.SimpleIndexDeclarationContext):
            ret.update(self._enterSimpleIndexDeclaration(child))

    @iterchild
    def _enterSimpleIndexDeclaration(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            ret[INDEX_NAME] = self._get_last_name(child)
        if isinstance(child, MySqlParser.IndexColumnNamesContext):
            ret['columns'] = self._enterIndexColumnNames(child).get('columns', [])

    @iterchild
    def _enterConstraintDeclaration(self, child, ret):
        if isinstance(child, MySqlParser.PrimaryKeyTableConstraintContext):
            ret[PRIMARY_KEY] = self._enterPrimaryKeyTableConstraint(child)
        if isinstance(child, MySqlParser.UniqueKeyTableConstraintContext):
            ret[UNIQUE_KEY] = self._enterUniqueKeyTableConstraint(child)

    @iterchild
    def _enterUniqueKeyTableConstraint(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            ret[INDEX_NAME] = self._get_last_name(child)
        if isinstance(child, MySqlParser.IndexColumnNamesContext):
            ret['columns'] = self._enterIndexColumnNames(child).get('columns', [])

    @iterchild
    def _enterPrimaryKeyTableConstraint(self, child, ret):
        if isinstance(child, MySqlParser.IndexColumnNamesContext):
            ret['columns'] = self._enterIndexColumnNames(child).get('columns', [])

    @iterchild
    def _enterColumnDeclaration(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            ret[COLUMN_NAME] = self._get_last_name(child)
        if isinstance(child, MySqlParser.ColumnDefinitionContext):
            ret[COLUMN_DEFINITION] = self._enterColumnDefinition(child)
