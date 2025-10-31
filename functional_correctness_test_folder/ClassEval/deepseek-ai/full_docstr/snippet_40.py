
from collections import deque
import decimal


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
        stack = deque()
        for elem in self.postfix_stack:
            if not self.is_operator(elem):
                stack.append(elem)
            else:
                second_value = stack.pop()
                first_value = stack.pop()
                result = self._calculate(first_value, second_value, elem)
                stack.append(str(result))
        return float(stack.pop())

    def prepare(self, expression):
        """
        Prepare the infix expression for conversion to postfix notation
        :param expression: string, the infix expression to be prepared
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.prepare("2+3*4")
        expression_calculator.postfix_stack = ['2', '3', '4', '*', '+']
        """
        expression = self.transform(expression)
        op_stack = deque()
        num_stack = deque()
        i = 0
        while i < len(expression):
            c = expression[i]
            if c == ' ':
                i += 1
                continue
            if not self.is_operator(c):
                num = ''
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num += expression[i]
                    i += 1
                num_stack.append(num)
            else:
                if c == '(':
                    op_stack.append(c)
                elif c == ')':
                    while op_stack[-1] != '(':
                        num_stack.append(op_stack.pop())
                    op_stack.pop()
                else:
                    while op_stack and op_stack[-1] != '(' and self.compare(op_stack[-1], c):
                        num_stack.append(op_stack.pop())
                    op_stack.append(c)
                i += 1
        while op_stack:
            num_stack.append(op_stack.pop())
        self.postfix_stack = num_stack

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
        op_map = {'+': 0, '-': 1, '*': 2, '/': 3, '(': 4, ')': 5, '%': 6}
        return self.operat_priority[op_map[peek]] >= self.operat_priority[op_map[cur]]

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
        first = decimal.Decimal(first_value)
        second = decimal.Decimal(second_value)
        if current_op == '+':
            return float(first + second)
        elif current_op == '-':
            return float(first - second)
        elif current_op == '*':
            return float(first * second)
        elif current_op == '/':
            return float(first / second)
        elif current_op == '%':
            return float(first % second)
        else:
            raise ValueError("Unsupported operator")

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
