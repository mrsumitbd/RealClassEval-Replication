
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
        # Operator precedence mapping
        self._priority = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '%': 2,
            '(': 0,
            ')': 0
        }

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
        stack = []
        for token in self.postfix_stack:
            if not self.is_operator(token):
                stack.append(float(token))
            else:
                b = stack.pop()
                a = stack.pop()
                res = self._calculate(str(a), str(b), token)
                stack.append(res)
        return float(stack[0]) if stack else 0.0

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
        op_stack = []
        i = 0
        n = len(expr)
        while i < n:
            c = expr[i]
            if c.isdigit() or c == '.':
                num = []
                while i < n and (expr[i].isdigit() or expr[i] == '.'):
                    num.append(expr[i])
                    i += 1
                output.append(''.join(num))
                continue
            elif self.is_operator(c):
                if c == '(':
                    op_stack.append(c)
                elif c == ')':
                    while op_stack and op_stack[-1] != '(':
                        output.append(op_stack.pop())
                    if op_stack and op_stack[-1] == '(':
                        op_stack.pop()
                else:
                    while (op_stack and op_stack[-1] != '(' and
                           self.compare(op_stack[-1], c)):
                        output.append(op_stack.pop())
                    op_stack.append(c)
            i += 1
        while op_stack:
            output.append(op_stack.pop())
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
        return c in {'+', '-', '*', '/', '(', ')', '%'}

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
        return self._priority[peek] >= self._priority[cur]

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
        elif current_op == '-':
            return a - b
        elif current_op == '*':
            return a * b
        elif current_op == '/':
            return a / b
        elif current_op == '%':
            return a % b
        else:
            raise ValueError("Unknown operator: " + current_op)

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
        return expression.replace(' ', '')
