from pyparsing import Forward, Group, Keyword, Literal, Optional, ParseException, ParserElement, QuotedString, Regex, Suppress, Word, infixNotation, opAssoc, printables

class SearchTerm:

    def __init__(self, tokens):
        self.tokens = tokens

    def __repr__(self):
        if 'singleterm' in self.tokens:
            tokens_fieldname = self.tokens.fieldname.replace('_.', 'attributes.')
            if self.tokens.fieldname == '_exists_':
                return f'{{"attributes.{self.tokens.singleterm}": {{"$exists": true}}}}'
            elif self.tokens.field[0] == '__default_field__':
                return f'{{"__default_field__": {{"__default_operator__": "{self.tokens.singleterm}", "$options": "i"}}}}'
            else:
                return f'{{"{tokens_fieldname}": {{"$regex": "{self.tokens.singleterm}", "$options": "i"}}}}'
        if 'phrase' in self.tokens:
            tokens_field0 = self.tokens.field[0].replace('_.', 'attributes.')
            if tokens_field0 == '__default_field__':
                return f'{{"__default_field__": {{"__default_operator__": "{self.tokens.phrase}", "$options": "i"}}}}'
            else:
                return f'{{"{tokens_field0}": {{"$regex": "\\\\b{self.tokens.phrase}\\\\b", "$options": "i"}}}}'
        if 'wildcard' in self.tokens:
            return f'{{"{self.tokens.field[0]}": {{"$regex": "\\\\b{self.tokens.wildcard}\\\\b", "$options": "i"}}}}'
        if 'regex' in self.tokens:
            return f'{{"{self.tokens.field[0]}": {{"$regex": "{self.tokens.regex}", "$options": "i"}}}}'

        def range_term(field, operator, range):
            if field in ['duplicateCount', 'timeout']:
                range = int(range)
            else:
                range = f'"{range}"'
            return f'{{"{field}": {{"{operator}": {range}}}}}'
        if 'range' in self.tokens:
            if self.tokens.range[0].lowerbound == '*':
                lower_term = '{}'
            else:
                lower_term = range_term(self.tokens.field[0], '$gte' if 'inclusive' in self.tokens.range[0] else '$gt', self.tokens.range[0].lowerbound)
            if self.tokens.range[2].upperbound == '*':
                upper_term = '{}'
            else:
                upper_term = range_term(self.tokens.field[0], '$lte' if 'inclusive' in self.tokens.range[2] else '$lt', self.tokens.range[2].upperbound)
            return f'{{"$and": [{lower_term}, {upper_term}]}}'
        if 'onesidedrange' in self.tokens:
            return range_term(self.tokens.field[0], self.tokens.onesidedrange.op, self.tokens.onesidedrange.bound)
        if 'subquery' in self.tokens:
            tokens_field0 = self.tokens.field[0].replace('_.', 'attributes.')
            if tokens_field0 != '__default_field__':
                return f'{self.tokens.subquery[0]}'.replace('__default_field__', tokens_field0).replace('__default_operator__', '$regex')
            else:
                return f'{self.tokens.subquery[0]}'
        raise ParseException(f'Search term did not match query syntax: {self.tokens}')