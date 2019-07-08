# -*- coding: utf-8 -*-

"""Main module."""

from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream
from antlr4.InputStream import InputStream

from MySqlLexer import MySqlLexer
from MySqlParser import MySqlParser
from MySqlParserListener import MySqlParserListener


class TABLE_ATTR_MAP(object):
    tablename = 'tablename'
    indexname = 'indexname'
    alluid = 'alluid'
    columnnames = 'columnnames'


class MyListener(MySqlParserListener):
    def __init__(self, handle):
        self.w_handle = handle

    # table name
    def enterTableName(self, ctx):
        value = ctx.getText()
        self.w_handle.set_interface(TABLE_ATTR_MAP.tablename, value)

    # table index Column Names
    def enterIndexColumnNames(self, ctx):
        value = ctx.getText()
        self.w_handle.set_interface(TABLE_ATTR_MAP.indexname, value)

    # statement uid
    def enterUid(self, ctx):
        value = ctx.getText()
        self.w_handle.set_interface(TABLE_ATTR_MAP.alluid, value)

        if not (isinstance(ctx.parentCtx, (
            MySqlParser.UniqueKeyTableConstraintContext,
            MySqlParser.ForeignKeyTableConstraintContext,
            MySqlParser.SimpleIndexDeclarationContext,
            MySqlParser.SpecialIndexDeclarationContext,
            MySqlParser.IndexColumnNameContext,
        )) or isinstance(ctx.parentCtx.parentCtx, MySqlParser.TableNameContext)):
            self.w_handle.set_interface(TABLE_ATTR_MAP.columnnames, value)

    # PrimaryKey Column
    def enterPrimaryKeyColumnConstraint(self, ctx):
        if isinstance(ctx.parentCtx.parentCtx, MySqlParser.ColumnDeclarationContext):
            value = ctx.parentCtx.parentCtx.children[0].getText()
            self.w_handle.set_interface(TABLE_ATTR_MAP.indexname, "({0})".format(value))

    # UniqueKey Column
    def enterUniqueKeyColumnConstraint(self, ctx):
        if isinstance(ctx.parentCtx.parentCtx, MySqlParser.ColumnDeclarationContext):
            value = ctx.parentCtx.parentCtx.children[0].getText()
            self.w_handle.set_interface(TABLE_ATTR_MAP.indexname, "({0})".format(value))


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
        self.sql = sql
        self.input_stream = CaseChangingCharInputStream(self.sql)
        self.lexer = MySqlLexer(self.input_stream)
        self.token_stream = CommonTokenStream(self.lexer)
        self.parser = MySqlParser(self.token_stream)
        self.tree = self.parser.root()
        self.printer = MyListener(self)
        self.walker = ParseTreeWalker()
        self.walker.walk(self.printer, self.tree)

    def set_interface(self, attr_type, value):
        attr = getattr(self, attr_type, [])
        attr.append(value)
        setattr(self, attr_type, attr)

    def get_tablename(self):
        return getattr(self, TABLE_ATTR_MAP.tablename, [])

    def get_indexname(self):
        return getattr(self, TABLE_ATTR_MAP.indexname, [])

    def get_alluid(self):
        return getattr(self, TABLE_ATTR_MAP.alluid, [])

    def get_columnnames(self):
        return getattr(self, TABLE_ATTR_MAP.columnnames, [])


def mysql_token_parser(sql):
    return SqlParseHandle(sql)


if __name__ == '__main__':
    creat_sql1 = u"""
        CREATE TABLE `aaa`.`t_zcm_operation_luck_award_record` (
  `id` bigint(20) NOT NULL COMMENT '主键id',
  `operation_seq` varchar(30) NOT NULL COMMENT '运营活动序列号',
  `award_user_id` bigint(20) NOT NULL COMMENT '中奖用户id',
  `award_type` int(11) DEFAULT NULL COMMENT '中奖奖品类型',
  `award_id` varchar(40) DEFAULT NULL UNIQUE KEY COMMENT '中奖奖品编号',
  `award_content` varchar(20)  DEFAULT NULL COMMENT '中奖内容',
  `award_reason` varchar(30)  DEFAULT NULL,
  `award_source` int(11) DEFAULT NULL COMMENT '中奖来源',
  `state` tinyint(4) NOT NULL PRIMARY KEY COMMENT '状态',
  `addtime` datetime NOT NULL COMMENT '新建时间',
  `updatetime` datetime NOT NULL COMMENT '更新时间',
  `ip` varchar(50)  DEFAULT NULL COMMENT '中奖者ip',
  `imei` varchar(50)  DEFAULT NULL COMMENT '中奖者设备号',
  `intext` int(11) DEFAULT NULL COMMENT '备用字段',
  `longext` bigint(20) DEFAULT NULL COMMENT '备用字段',
  `strext` varchar(200)  DEFAULT NULL COMMENT '备用字段',
  PRIMARY KEY (id),
  UNIQUE KEY `idx_op_seq_uid_type` (`operation_seq`,`award_user_id`,`award_type`),
  KEY `idx_op_uid_type` (`award_user_id`,`award_type`),
  KEY `idx_op_uid_sss` (longext(10))
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='招才猫幸运值系列活动中奖记录表';
    """

    alter_sql1 = u"ALTER TABLE t_a_gun2_6_dw_pfm_emp_cm ADD INDEX idx_eob_date(empid_org_bus (200),pfm_date);"
    alter_sql2 = u"ALTER TABLE tab_name ADD address  varchar(100) NOT NULL DEFAULT '' COMMENT '地址' AFTER  amount;"
    alter_sql3 = u"ALTER TABLE tab_name ADD address01  varchar(100) NOT NULL DEFAULT '' COMMENT '地址1' , ADD address02  varchar(100) NOT NULL DEFAULT '' COMMENT '地址2' ;"

    #### debug code
    sql = creat_sql1
    a = mysql_token_parser(sql)
    b = a.get_tablename()
    c = a.get_indexname()
    d = a.get_columnnames()
    print "table name:", b
    print "index name:", c
    print "column name:", d
