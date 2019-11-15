# coding: utf-8
from mysqltokenparser.utils import iterchild, CREATE_TABLE
from mysqltokenparser.MySqlParser import MySqlParser


class CreateTableMixin:
    def enterColumnCreateTable(self, ctx):
        data = {}
        self.ret['data'] = {
            'type': CREATE_TABLE,
            'data': data
        }

        children = ctx.children
        for child in children:
            if isinstance(child, MySqlParser.TableNameContext):
                data['tablename'] = self._get_last_name(child)
            if isinstance(child, MySqlParser.CreateDefinitionsContext):
                data['createdefinitions'] = self._enterCreateDefinitions(child)
            if isinstance(child, MySqlParser.TableOptionEngineContext):
                data.update(self._enterTableOptionEngine(child))
            if isinstance(child, MySqlParser.TableOptionCharsetContext):
                data.update(self._enterTableOptionCharset(child))

    @iterchild
    def _enterTableOptionCharset(self, child, ret):
        if isinstance(child, MySqlParser.CharsetNameContext):
            ret['charset'] = self._get_last_name(child)

    @iterchild
    def _enterTableOptionEngine(self, child, ret):
        if isinstance(child, MySqlParser.EngineNameContext):
            ret['engine'] = self._get_last_name(child)

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
            indexs.setdefault('common_key', []).append(self._enterIndexDeclaration(child))

    @iterchild
    def _enterIndexDeclaration(self, child, ret):
        # common_key = ret.setdefault('common_key', [])
        if isinstance(child, MySqlParser.SimpleIndexDeclarationContext):
            ret.update(self._enterSimpleIndexDeclaration(child))

    @iterchild
    def _enterSimpleIndexDeclaration(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            ret['indexname'] = self._get_last_name(child)
        if isinstance(child, MySqlParser.IndexColumnNamesContext):
            ret['columnnames'] = self._enterIndexColumnNames(child).get('columns', [])

    @iterchild
    def _enterConstraintDeclaration(self, child, ret):
        if isinstance(child, MySqlParser.PrimaryKeyTableConstraintContext):
            ret['primary_key'] = self._enterPrimaryKeyTableConstraint(child)
        if isinstance(child, MySqlParser.UniqueKeyTableConstraintContext):
            ret['unique_key'] = self._enterUniqueKeyTableConstraint(child)

    @iterchild
    def _enterUniqueKeyTableConstraint(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            ret['indexname'] = self._get_last_name(child)
        if isinstance(child, MySqlParser.IndexColumnNamesContext):
            ret['columns'] = self._enterIndexColumnNames(child).get('columns', [])

    @iterchild
    def _enterPrimaryKeyTableConstraint(self, child, ret):
        if isinstance(child, MySqlParser.IndexColumnNamesContext):
            ret['columns'] = self._enterIndexColumnNames(child).get('columns', [])

    @iterchild
    def _enterColumnDeclaration(self, child, ret):
        if isinstance(child, MySqlParser.UidContext):
            ret['columnname'] = self._get_last_name(child)
        if isinstance(child, MySqlParser.ColumnDefinitionContext):
            ret['columndefinition'] = self._enterColumnDefinition(child)
