import re

class ExpressionParser:

    def __init__(self, expr_str):
        self.expr_str = expr_str
        self.pos = 0
        self.tokens = self._tokenize(expr_str)
        self.current_token = 0

    def _tokenize(self, expr_str):
        tokens = []
        i = 0
        while i < len(expr_str):
            if expr_str[i].isspace():
                i += 1
                continue
            elif expr_str[i] == '(':
                tokens.append('(')
                i += 1
            elif expr_str[i] == ')':
                tokens.append(')')
                i += 1
            elif self._is_logical_operator(expr_str, i, 'and'):
                tokens.append('and')
                i += 3
            elif self._is_logical_operator(expr_str, i, 'or'):
                tokens.append('or')
                i += 2
            elif expr_str[i:i + 8] == 're.match':
                j = i
                paren_count = 0
                while j < len(expr_str):
                    if expr_str[j] == '(':
                        paren_count += 1
                    elif expr_str[j] == ')':
                        paren_count -= 1
                        if paren_count == 0:
                            break
                    j += 1
                if j < len(expr_str):
                    tokens.append(expr_str[i:j + 1])
                    i = j + 1
                else:
                    raise ValueError('Unmatched parentheses in regex expression')
            else:
                j = i
                while j < len(expr_str) and expr_str[j] not in '()' and (not self._is_logical_operator(expr_str, j, 'and')) and (not self._is_logical_operator(expr_str, j, 'or')):
                    j += 1
                if i != j:
                    expr = expr_str[i:j].strip()
                    if expr:
                        tokens.append(expr)
                i = j
        return tokens

    def _is_logical_operator(self, expr_str, pos, operator):
        """
        check if the specified position is a logical operator (not part of a variable name)

        Args:
            expr_str: expression string
            pos: current position
            operator: the operator to check ('and' or 'or')

        Returns:
            bool: if it is a standalone logical operator, return True, otherwise return False
        """
        op_len = len(operator)
        if pos + op_len > len(expr_str):
            return False
        if expr_str[pos:pos + op_len].lower() != operator.lower():
            return False
        if pos > 0:
            prev_char = expr_str[pos - 1]
            if prev_char.isalnum() or prev_char in '_.':
                return False
        if pos + op_len < len(expr_str):
            next_char = expr_str[pos + op_len]
            if next_char.isalnum() or next_char in '_.':
                return False
        return True

    def parse(self):
        return self._parse_expression()

    def _parse_expression(self):
        return self._parse_or()

    def _parse_or(self):
        left = self._parse_and()
        while self.current_token < len(self.tokens) and self.tokens[self.current_token] == 'or':
            self.current_token += 1
            right = self._parse_and()
            left = {'type': 'or', 'left': left, 'right': right}
        return left

    def _parse_and(self):
        left = self._parse_primary()
        while self.current_token < len(self.tokens) and self.tokens[self.current_token] == 'and':
            self.current_token += 1
            right = self._parse_primary()
            left = {'type': 'and', 'left': left, 'right': right}
        return left

    def _parse_primary(self):
        if self.current_token >= len(self.tokens):
            raise ValueError('Incomplete expression')
        token = self.tokens[self.current_token]
        self.current_token += 1
        if token == '(':
            expr = self._parse_expression()
            if self.current_token >= len(self.tokens) or self.tokens[self.current_token] != ')':
                raise ValueError('Unmatched parentheses')
            self.current_token += 1
            return expr
        elif token.startswith('re.match'):
            match = re.match('re\\.match\\((.*?), (.*?)\\)', token)
            if match:
                pattern = match.group(1)
                arg_name = match.group(2)
                return {'type': 'regex', 'pattern': pattern, 'arg_name': arg_name}
            else:
                raise ValueError(f'Invalid regex expression: {token}')
        else:
            if '==' in token:
                parts = token.split('==')
                if len(parts) == 2:
                    return {'type': 'eq', 'left': parts[0].strip(), 'right': parts[1].strip()}
            elif '!=' in token:
                parts = token.split('!=')
                if len(parts) == 2:
                    return {'type': 'neq', 'left': parts[0].strip(), 'right': parts[1].strip()}
            elif '>=' in token:
                parts = token.split('>=')
                if len(parts) == 2:
                    return {'type': 'ge', 'left': parts[0].strip(), 'right': parts[1].strip()}
            elif '<=' in token:
                parts = token.split('<=')
                if len(parts) == 2:
                    return {'type': 'le', 'left': parts[0].strip(), 'right': parts[1].strip()}
            elif '>' in token:
                parts = token.split('>')
                if len(parts) == 2:
                    return {'type': 'gt', 'left': parts[0].strip(), 'right': parts[1].strip()}
            elif '<' in token:
                parts = token.split('<')
                if len(parts) == 2:
                    return {'type': 'lt', 'left': parts[0].strip(), 'right': parts[1].strip()}
            raise ValueError(f'Unable to parse expression: {token}')