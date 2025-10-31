from pyparsing import Forward, Group, Keyword, Literal, Optional, ParseException, ParserElement, QuotedString, Regex, Suppress, Word, infixNotation, opAssoc, printables

class SearchTerm:

    def __init__(self, tokens):
        self.tokens = tokens

    def __repr__(self):
        if 'singleterm' in self.tokens:
            if self.tokens.fieldname == '_exists_':
                return f""""attributes"::jsonb ? '{self.tokens.singleterm}'"""
            elif self.tokens.fieldname in ['correlate', 'service', 'tags']:
                return f''''{self.tokens.singleterm}'=ANY("{self.tokens.field[0]}")'''
            elif self.tokens.attr:
                tokens_attr = self.tokens.attr.replace('_', 'attributes')
                return f""""{tokens_attr}"::jsonb ->>'{self.tokens.fieldname}' ILIKE '%%{self.tokens.singleterm}%%'"""
            else:
                return f""""{self.tokens.field[0]}" ILIKE '%%{self.tokens.singleterm}%%'"""
        if 'phrase' in self.tokens:
            if self.tokens.field[0] == '__default_field__':
                return f""""__default_field__" ~* '\\y{self.tokens.phrase}\\y'"""
            elif self.tokens.field[0] in ['correlate', 'service', 'tags']:
                return f''''{self.tokens.phrase}'=ANY("{self.tokens.field[0]}")'''
            elif self.tokens.attr:
                tokens_attr = self.tokens.attr.replace('_', 'attributes')
                return f""""{tokens_attr}"::jsonb ->>'{self.tokens.fieldname}' ~* '\\y{self.tokens.phrase}\\y'"""
            else:
                return f""""{self.tokens.field[0]}" ~* '\\y{self.tokens.phrase}\\y'"""
        if 'wildcard' in self.tokens:
            return f""""{self.tokens.field[0]}" ~* '\\y{self.tokens.wildcard}\\y'"""
        if 'regex' in self.tokens:
            return f""""{self.tokens.field[0]}" ~* '{self.tokens.regex}'"""
        if 'range' in self.tokens:
            if self.tokens.range[0].lowerbound == '*':
                lower_term = '1=1'
            else:
                lower_term = '"{}" {} \'{}\''.format(self.tokens.field[0], '>=' if 'inclusive' in self.tokens.range[0] else '>', self.tokens.range[0].lowerbound)
            if self.tokens.range[2].upperbound == '*':
                upper_term = '1=1'
            else:
                upper_term = '"{}" {} \'{}\''.format(self.tokens.field[0], '<=' if 'inclusive' in self.tokens.range[2] else '<', self.tokens.range[2].upperbound)
            return f'({lower_term} AND {upper_term})'
        if 'onesidedrange' in self.tokens:
            return '("{}" {} \'{}\')'.format(self.tokens.field[0], self.tokens.onesidedrange.op, self.tokens.onesidedrange.bound)
        if 'subquery' in self.tokens:
            if self.tokens.attr:
                tokens_attr = 'attributes' if self.tokens.attr == '_' else self.tokens.attr
                tokens_fieldname = f""""{tokens_attr}"::jsonb ->>'{self.tokens.fieldname}'"""
            else:
                tokens_fieldname = f'"{self.tokens.fieldname or self.tokens.field[0]}"'
            return f'{self.tokens.subquery[0]}'.replace('"__default_field__"', tokens_fieldname)
        raise ParseException(f'Search term did not match query syntax: {self.tokens}')