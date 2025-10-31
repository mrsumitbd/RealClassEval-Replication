class Calculator:
    """
    This is a class for a calculator, capable of performing basic arithmetic calculations on numerical expressions using the operators +, -, *, /, and ^ (exponentiation).
    """

    def __init__(self):
        """
        Initialize the operations performed by the five operators'+','-','*','/','^'
        """
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '^': lambda x, y: x ** y
        }

    def calculate(self, expression):
        """
        Calculate the value of a given expression
        :param expression: string, given expression
        :return:If successful, returns the value of the expression; otherwise, returns None
        >>> calculator = Calculator()
        >>> calculator.calculate('1+2-3')
        0.0
        """
        if not isinstance(expression, str):
            return None

        try:
            tokens = self._tokenize(expression)
            operand_stack = []
            operator_stack = []

            def apply_until(predicate):
                while operator_stack and predicate(operator_stack[-1]):
                    self.apply_operator(operand_stack, operator_stack)

            prev_token_type = None  # 'num' or 'op'
            i = 0
            while i < len(tokens):
                tok = tokens[i]
                if isinstance(tok, float):
                    operand_stack.append(tok)
                    prev_token_type = 'num'
                else:
                    # operator
                    op = tok
                    # right-associative for '^'
                    apply_until(lambda top: (self.precedence(top) > self.precedence(op)) or
                                (self.precedence(top) == self.precedence(op) and op != '^'))
                    operator_stack.append(op)
                    prev_token_type = 'op'
                i += 1

            while operator_stack:
                self.apply_operator(operand_stack, operator_stack)

            if len(operand_stack) != 1:
                return None
            return float(operand_stack[0])
        except Exception:
            return None

    def precedence(self, operator):
        """
        Returns the priority of the specified operator, where the higher the priority, the greater the assignment. The priority of '^' is greater than '/' and '*', and the priority of '/' and '*' is greater than '+' and '-'
        :param operator: string, given operator
        :return: int, the priority of the given operator, otherwise return 0
        >>> calculator = Calculator()
        >>> calculator.precedence('+')
        1
        >>> calculator.precedence('^')
        3
        """
        if operator in ('+', '-'):
            return 1
        if operator in ('*', '/'):
            return 2
        if operator == '^':
            return 3
        return 0

    def apply_operator(self, operand_stack, operator_stack):
        """
        Use the operator at the top of the operator stack to perform the operation on the two numbers at the top of the operator stack, and store the results at the top of the operator stack
        :param operand_stack:list
        :param operator_stack:list
        :return: the updated operand_stack and operator_stack
        >>> calculator = Calculator()
        >>> calculator.apply_operator([1, 2, 3], ['+', '-'])
        ([1, -1], ['+'])
        """
        if not operator_stack or len(operand_stack) < 2:
            return operand_stack, operator_stack
        op = operator_stack.pop()
        right = float(operand_stack.pop())
        left = float(operand_stack.pop())
        # Handle division by zero explicitly to avoid exceptions propagating in some contexts
        if op == '/' and right == 0:
            raise ZeroDivisionError("division by zero")
        result = self.operators[op](left, right)
        operand_stack.append(result)
        return operand_stack, operator_stack

    def _tokenize(self, expression):
        s = expression.replace(' ', '')
        tokens = []
        i = 0
        n = len(s)

        def read_number(start):
            j = start
            dot_count = 0
            while j < n and (s[j].isdigit() or s[j] == '.'):
                if s[j] == '.':
                    dot_count += 1
                    if dot_count > 1:
                        break
                j += 1
            num_str = s[start:j]
            if num_str in ('', '.', '+', '-'):
                raise ValueError("Invalid number")
            return float(num_str), j

        while i < n:
            ch = s[i]
            if ch.isdigit() or ch == '.':
                num, i = read_number(i)
                tokens.append(num)
                continue
            if ch in self.operators:
                # unary sign handling for '-' and '+' (e.g., -3.5+2 or 3*-2)
                if ch in '+-' and (len(tokens) == 0 or isinstance(tokens[-1], str)):
                    # look ahead for a number
                    j = i + 1
                    if j < n and (s[j].isdigit() or s[j] == '.'):
                        num, i2 = read_number(j)
                        if ch == '-':
                            num = -num
                        tokens.append(num)
                        i = i2
                        continue
                tokens.append(ch)
                i += 1
                continue
            else:
                raise ValueError("Invalid character")
        return tokens
