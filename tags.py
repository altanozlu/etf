import functools

__author__ = 'ahawker'

NEW_FLOAT     = 70
BIT_BINARY    = 77
COMPRESSED    = 80
SMALL_INTEGER = 97
INTEGER       = 98
FLOAT         = 99
ATOM          = 100
REFERENCE     = 101
PORT          = 102
PID           = 103
SMALL_TUPLE   = 104
LARGE_TUPLE   = 105
NIL           = 106
STRING        = 107
LIST          = 108
BINARY        = 109
SMALL_BIG     = 110
LARGE_BIG     = 111
NEW_FUN       = 112
EXPORT        = 113
NEW_REFERENCE = 114
SMALL_ATOM    = 115
FUN           = 117
VERSION       = 131

def tag(tag):
    def decorator(func):
        @functools.wraps(func)
        def f(*args, **kwargs):
            return func(*args, **kwargs)
        f.tag = tag
        return f
    return decorator