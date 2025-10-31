import re

class SedStatementParser:

    def __init__(self, statement):
        self.statement = statement

    def parse(self):
        if not self.statement.startswith('s'):
            raise Exception("Transform statement must start with 's' {!r}".format(self.statement))
        statement = self.statement[1:]
        separator = statement[0]
        if not statement.endswith(separator):
            raise Exception('Transform statement must end with separator {!r} ({!r})'.format(separator, statement))
        tokens = self.tokenize_string(statement[1:-1], separator)
        if len(tokens) != 2:
            raise Exception('Bad transform statement, must have search and replace expressions {!r}'.format(statement))
        search = tokens[0]
        replace = tokens[1]
        search = self.reverse_escaping(search)
        return (re.compile(search), replace)

    @classmethod
    def reverse_escaping(cls, string):
        found_escape = False
        output = ''
        for c in string:
            if c == '\\':
                if found_escape:
                    output += '\\\\'
                    found_escape = False
                else:
                    found_escape = True
            elif found_escape:
                if c not in '{}()+?|':
                    output += '\\'
                output += c
                found_escape = False
            elif c in '{}()+?|':
                output += '\\' + c
            else:
                output += c
        return output

    @classmethod
    def tokenize_string(cls, string, separator):
        """Split string with given separator unless the separator is escaped with backslash"""
        results = []
        token = ''
        found_escape = False
        for c in string:
            if found_escape:
                if c == separator:
                    token += separator
                else:
                    token += '\\' + c
                found_escape = False
                continue
            if c == '\\':
                found_escape = True
            elif c == separator:
                results.append(token)
                token = ''
            else:
                token += c
        results.append(token)
        return results