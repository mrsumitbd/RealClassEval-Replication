from collections import deque


class ExpressionCalculator:
    """
    This is a class in Python that can perform calculations with basic arithmetic operations, including addition, subtraction, multiplication, division, and modulo.
    """

    def __init__(self):
        """
        Initialize the expression calculator
        """
        self.postfix_stack = deque()
        self.operat_priority = [0, 3, 2, 1, -1, 1, 0, 2]

    def calculate(self, expression):
        """
        Calculate the result of the given postfix expression
        :param expression: string, the postfix expression to be calculated
        :return: float, the calculated result
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.calculate("2 + 3 * 4")
        14.0

        """
        self.prepare(expression)
        eval_stack = []
        for token in self.postfix_stack:
            if not self.is_operator(token):
                eval_stack.append(float(token))
            else:
                b = eval_stack.pop()
                a = eval_stack.pop()
                res = self._calculate(a, b, token)
                eval_stack.append(res)
        return float(eval_stack[-1]) if eval_stack else 0.0

    def prepare(self, expression):
        """
        Prepare the infix expression for conversion to postfix notation
        :param expression: string, the infix expression to be prepared
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.prepare("2+3*4")

        expression_calculator.postfix_stack = ['2', '3', '4', '*', '+']
        """
        expr = self.transform(expression)
        output = []
        ops = []

        i = 0
        n = len(expr)
        prev_token_type = None  # 'num', 'op', 'lparen', 'rparen'
        while i < n:
            ch = expr[i]

            if ch.isdigit() or ch == '.':
                j = i
                while j < n and (expr[j].isdigit() or expr[j] == '.'):
                    j += 1
                number = expr[i:j]
                output.append(number)
                prev_token_type = 'num'
                i = j
                continue

            # handle unary minus
            if ch == '-' and (prev_token_type in (None, 'op', 'lparen')):
                # read signed number
                j = i + 1
                if j < n and (expr[j].isdigit() or expr[j] == '.'):
                    k = j
                    while k < n and (expr[k].isdigit() or expr[k] == '.'):
                        k += 1
                    number = '-' + expr[j:k]
                    output.append(number)
                    prev_token_type = 'num'
                    i = k
                    continue
                # if not followed by number, treat as operator
            if ch in '+-*/%':
                while ops and ops[-1] != '(' and self.compare(ops[-1], ch):
                    output.append(ops.pop())
                ops.append(ch)
                prev_token_type = 'op'
                i += 1
                continue
            if ch == '(':
                ops.append(ch)
                prev_token_type = 'lparen'
                i += 1
                continue
            if ch == ')':
                while ops and ops[-1] != '(':
                    output.append(ops.pop())
                if ops and ops[-1] == '(':
                    ops.pop()
                prev_token_type = 'rparen'
                i += 1
                continue

            # Unknown character (skip)
            i += 1

        while ops:
            output.append(ops.pop())

        self.postfix_stack = output

    @staticmethod
    def is_operator(c):
        """
        Check if a character is an operator in {'+', '-', '*', '/', '(', ')', '%'}
        :param c: string, the character to be checked
        :return: bool, True if the character is an operator, False otherwise
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.is_operator("+")
        True

        """
        return c in {"+", "-", "*", "/", "%", "(", ")"}

    def compare(self, peek, cur):
        """
        Compare the precedence of two operators
        :param cur: string, the current operator
        :param peek: string, the operator at the top of the operator stack
        :return: bool, True if the current operator has higher or equal precedence, False otherwise
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.compare("+", "-")
        True

        """
        precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '%': 2,
        }
        if peek == '(':
            return False
        return precedence.get(peek, -1) >= precedence.get(cur, -1)

    @staticmethod
    def _calculate(first_value, second_value, current_op):
        """
        Perform the mathematical calculation based on the given operands and operator
        :param first_value: string, the first operand
        :param second_value: string, the second operand
        :param current_op: string, the operator
        :return: decimal.Decimal, the calculated result
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator._calculate("2", "3", "+")
        5.0

        """
        a = float(first_value)
        b = float(second_value)
        if current_op == '+':
            return a + b
        if current_op == '-':
            return a - b
        if current_op == '*':
            return a * b
        if current_op == '/':
            return a / b
        if current_op == '%':
            return a % b
        raise ValueError("Unsupported operator: {}".format(current_op))

    @staticmethod
    def transform(expression):
        """
        Transform the infix expression to a format suitable for conversion
        :param expression: string, the infix expression to be transformed
        :return: string, the transformed expression
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.transform("2 + 3 * 4")
        "2+3*4"

        """
        return "".join(expression.split())
