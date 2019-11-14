# coding: utf-8
from functools import wraps


def iterchild(func):
    @wraps(func)
    def wrapped(self, ctx, *args, **kwargs):
        ret = {}
        children = ctx.children
        for child in children:
            func(self, child, ret)
        return ret
    return wrapped
