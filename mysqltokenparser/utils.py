# coding: utf-8
from functools import wraps

ALTER_TABLE= 'altertable'
ADD_COLUMN = 'addcolumn'
MODIFY_COLUMN = 'modifycolumn'
CHANGE_COLUMN = 'changecolumn'
ADD_INDEX = 'addindex'
DROP_COLUMN = 'dropcolumn'

CREATE_TABLE = 'createtable'


def iterchild(func):
    @wraps(func)
    def wrapped(self, ctx, *args, **kwargs):
        ret = {}
        children = ctx.children
        for child in children:
            func(self, child, ret)
        return ret
    return wrapped
