# coding: utf-8

# sql type
SQL_TYPE_DDL = 'ddl'
SQL_TYPE_DML = 'dml'
SQL_TYPE_TRANSACTION = 'transaction'
SQL_TYPE_REPLICATION = 'replication'
SQL_TYPE_PREPARED = 'prepared'
SQL_TYPE_ADMINISTRATION = 'administration'
SQL_TYPE_UTILITY = 'utility'

# ddl type
DDL_TYPE_CREATEDATABASE = 'createdatabase'
DDL_TYPE_CREATEEVENT = 'createevent'
DDL_TYPE_CREATEINDEX = 'createindex'
DDL_TYPE_CREATELOGFILEGROUP = 'createlogfilegroup'
DDL_TYPE_CREATEPROCEDURE = 'createprocedure'
DDL_TYPE_CREATEFUNCTION = 'createfunction'
DDL_TYPE_CREATESERVER = 'createserver'
DDL_TYPE_CREATETABLE = 'createtable'
DDL_TYPE_CREATETABLESPACEINNODB = 'createtablespaceinnodb'
DDL_TYPE_CREATETABLESPACENDB = 'createtablespacendb'
DDL_TYPE_CREATETRIGGER = 'createtrigger'
DDL_TYPE_CREATEVIEW = 'createview'
DDL_TYPE_ALTERDATABASE = 'alterdatabase'
DDL_TYPE_ALTEREVENT = 'alterevent'
DDL_TYPE_ALTERFUNCTION = 'alterfunction'
DDL_TYPE_ALTERINSTANCE = 'alterinstance'
DDL_TYPE_ALTERLOGFILEGROUP = 'alterlogfilegroup'
DDL_TYPE_ALTERPROCEDURE = 'alterprocedure'
DDL_TYPE_ALTERSERVER = 'alterserver'
DDL_TYPE_ALTERTABLE = 'altertable'
DDL_TYPE_ALTERTABLESPACE = 'altertablespace'
DDL_TYPE_ALTERVIEW = 'alterview'
DDL_TYPE_DROPDATABASE = 'dropdatabase'
DDL_TYPE_DROPEVENT = 'dropevent'
DDL_TYPE_DROPINDEX = 'dropindex'
DDL_TYPE_DROPLOGFILEGROUP = 'droplogfilegroup'
DDL_TYPE_DROPPROCEDURE = 'dropprocedure'
DDL_TYPE_DROPFUNCTION = 'dropfunction'
DDL_TYPE_DROPSERVER = 'dropserver'
DDL_TYPE_DROPTABLE = 'droptable'
DDL_TYPE_DROPTABLESPACE = 'droptablespace'
DDL_TYPE_DROPTRIGGER = 'droptrigger'
DDL_TYPE_DROPVIEW = 'dropview'
DDL_TYPE_RENAMETABLE = 'renametable'
DDL_TYPE_TRUNCATETABLE = 'truncatetable'

# dml type
DML_TYPE_SELECTSTATEMENT = 'select'
DML_TYPE_INSERTSTATEMENT = 'insert'
DML_TYPE_UPDATESTATEMENT = 'update'
DML_TYPE_DELETESTATEMENT = 'delete'
DML_TYPE_REPLACESTATEMENT = 'replace'
DML_TYPE_CALLSTATEMENT = 'call'
DML_TYPE_LOADDATASTATEMENT = 'loaddata'
DML_TYPE_LOADXMLSTATEMENT = 'loadxml'
DML_TYPE_DOSTATEMENT = 'do'
DML_TYPE_HANDLERSTATEMENT = 'handler'

# table option
TABLE_OPTION_ENGINE = 'engine'
TABLE_OPTION_AUTOINCREMENT = 'autoincrement'
TABLE_OPTION_AVERAGE = 'average'
TABLE_OPTION_CHARSET = 'charset'
TABLE_OPTION_CHECKSUM = 'checksum'
TABLE_OPTION_COLLATE = 'collate'
TABLE_OPTION_COMMENT = 'comment'
TABLE_OPTION_COMPRESSION = 'compression'
TABLE_OPTION_CONNECTION = 'connection'
TABLE_OPTION_DATADIRECTORY = 'datadirectory'
TABLE_OPTION_DELAY = 'delay'
TABLE_OPTION_ENCRYPTION = 'encryption'
TABLE_OPTION_INDEXDIRECTORY = 'indexdirectory'
TABLE_OPTION_INSERTMETHOD = 'insertmethod'
TABLE_OPTION_KEYBLOCKSIZE = 'keyblocksize'
TABLE_OPTION_MAXROWS = 'maxrows'
TABLE_OPTION_MINROWS = 'minrows'
TABLE_OPTION_PACKKEYS = 'packkeys'
TABLE_OPTION_PASSWORD = 'password'
TABLE_OPTION_ROWFORMAT = 'rowformat'
TABLE_OPTION_RECALCULATION = 'recalculation'
TABLE_OPTION_PERSISTENT = 'persistent'
TABLE_OPTION_SAMPLEPAGE = 'samplepage'
TABLE_OPTION_TABLESPACE = 'tablespace'
TABLE_OPTION_UNION = 'union'
