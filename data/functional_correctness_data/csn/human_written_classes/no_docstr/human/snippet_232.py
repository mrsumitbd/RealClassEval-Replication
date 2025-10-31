from PyQt6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat

class Formatter:

    def __init__(self, funcs=None):
        self._funcs = funcs or []

    def __or__(self, other):
        result = Formatter(self._funcs.copy())
        if isinstance(other, Formatter):
            result._funcs.extend(other._funcs)
        elif isinstance(other, QFont.Weight):
            result._funcs.append(lambda f: f.setFontWeight(other))
        return result

    def format(self, charFormat):
        for func in self._funcs:
            func(charFormat)