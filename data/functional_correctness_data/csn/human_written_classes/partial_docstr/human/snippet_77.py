class ParsingContext:
    """
    Class for determining where to split rmd options
    """
    parenthesis_count = 0
    curly_bracket_count = 0
    square_bracket_count = 0
    in_single_quote = False
    in_double_quote = False

    def __init__(self, line):
        self.line = line

    def in_global_expression(self):
        """Currently inside an expression"""
        return self.parenthesis_count == 0 and self.curly_bracket_count == 0 and (self.square_bracket_count == 0) and (not self.in_single_quote) and (not self.in_double_quote)

    def count_special_chars(self, char, prev_char):
        """Update parenthesis counters"""
        if char == '(':
            self.parenthesis_count += 1
        elif char == ')':
            self.parenthesis_count -= 1
            if self.parenthesis_count < 0:
                raise RMarkdownOptionParsingError(f'Option line "{self.line}" has too many closing parentheses')
        elif char == '{':
            self.curly_bracket_count += 1
        elif char == '}':
            self.curly_bracket_count -= 1
            if self.curly_bracket_count < 0:
                raise RMarkdownOptionParsingError(f'Option line "{self.line}" has too many closing curly brackets')
        elif char == '[':
            self.square_bracket_count += 1
        elif char == ']':
            self.square_bracket_count -= 1
            if self.square_bracket_count < 0:
                raise RMarkdownOptionParsingError(f'Option line "{self.line}" has too many closing square brackets')
        elif char == "'" and prev_char != '\\' and (not self.in_double_quote):
            self.in_single_quote = not self.in_single_quote
        elif char == '"' and prev_char != '\\' and (not self.in_single_quote):
            self.in_double_quote = not self.in_double_quote