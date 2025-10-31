
from collections import deque
from decimal import Decimal, getcontext


class ExpressionCalculator:
    """
    This is a class in Python that can perform calculations with basic arithmetic operations,
    including addition, subtraction, multiplication, division, and modulo.
    """

    def __init__(self):
        """
        Initialize the expression calculator
        """
        self.postfix_stack = deque()
        # Priority mapping: '(' lowest, then +/-, then */%
        self._priority = {'+': 1, '-': 1, '*': 2,
                          '/': 2, '%': 2, '(': 0, ')': 0}

    def calculate(self, expression):
        """
        Calculate the result of the given postfix expression
        :param expression: string, the postfix expression to be calculated
        :return: float, the calculated result
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.calculate("2 + 3 * 4")
        14.0
        """
        # Prepare the expression into postfix tokens
        self.prepare(expression)
        # Evaluate the postfix expression
        stack = []
        for token in self.postfix_stack:
            if token in self._priority:
                # Operator: pop two operands
                if len(stack) < 2:
                    raise ValueError("Invalid expression")
                second = stack.pop()
                first = stack.pop()
                result = self._calculate(first, second, token)
                stack.append(result)
            else:
                # Operand: push to stack
                stack.append(Decimal(token))
        if len(stack) != 1:
            raise ValueError("Invalid expression")
        return float(stack[0])

    def prepare(self, expression):
        """
        Prepare the infix expression for conversion to postfix notation
        :param expression: string, the infix expression to be prepared
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.prepare("2+3*4")
        >>> expression_calculator.postfix_stack
        ['2', '3', '4', '*', '+']
        """
        self.postfix_stack.clear()
        expr = self.transform(expression)
        i = 0
        n = len(expr)
        number = ''
        while i < n:
            c = expr[i]
            if c.isdigit() or c == '.':
                number += c
                i += 1
                continue
            if number:
                self.postfix_stack.append(number)
                number = ''
            if c in self._priority:
                if c == '(':
                    self.postfix_stack.append(c)
                elif c == ')':
                    # Pop until '('
                    while self.postfix_stack and self.postfix_stack[-1] != '(':
                        self.postfix_stack.append(self.postfix_stack.pop())
                    if not self.postfix_stack:
                        raise ValueError("Mismatched parentheses")
                    self.postfix_stack.pop()  # Remove '('
                else:
                    # Operator
                    while (self.postfix_stack and
                           self.postfix_stack[-1] != '(' and
                           self._priority[self.postfix_stack[-1]] >= self._priority[c]):
                        self.postfix_stack.append(self.postfix_stack.pop())
                    self.postfix_stack.append(c)
            else:
                # Ignore any other characters (e.g., spaces)
                pass
            i += 1
        if number:
            self.postfix_stack.append(number)
        # After processing, pop remaining operators
        while self.postfix_stack:
            op = self.postfix_stack.pop()
            if op in ('(', ')'):
                continue
            self.postfix_stack.append(op)

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
        return c in {'+', '-', '*', '/', '(', ')', '%'}

    def compare(self, cur, peek):
        """
        Compare the precedence of two operators
        :param cur: string, the current operator
        :param peek: string, the operator at the top of the operator stack
        :return: bool, True if the current operator has higher or equal precedence, False otherwise
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.compare("+", "-")
        True
        """
        return self._priority[cur] >= self._priority[peek]

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
        a = Decimal(first_value)
        b = Decimal(second_value)
        if current_op == '+':
            return a + b
        elif current_op == '-':
            return a - b
        elif current_op == '*':
            return a * b
        elif current_op == '/':
            if b == 0:
                raise ZeroDivisionError("division by zero")
            return a / b
        elif current_op == '%':
            if b == 0:
                raise ZeroDivisionError("modulo by zero")
            return a % b
        else:
            raise ValueError(f"Unsupported operator: {current_op}")

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
        return expression.replace(" ", "")
