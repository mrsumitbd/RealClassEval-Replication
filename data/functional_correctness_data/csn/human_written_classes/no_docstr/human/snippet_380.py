import re

class MultiFunctionCall:

    def __init__(self, func=None):
        self.__func__ = {} if func is None else func

    @staticmethod
    def default_func(session, string):
        return string

    def call(self, session, string):
        s = string.split(':')
        if len(s) <= 1:
            return string
        name = s[0].strip()
        s = ':'.join(s[1:])
        func = self.default_func
        try:
            func = self.__func__[name]
        except KeyError:
            s = string
        new_string = re.sub('([\\[\\]{}%:])', '\\\\\\1', s)
        return re.sub('\\\\([\\[\\]{}%:])', '\\1', func(session, new_string))