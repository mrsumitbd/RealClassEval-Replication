
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

        expr = expression.replace(' ', '')
        if not expr:
            return None

        operand_stack = []
        operator_stack = []

        i = 0
        n = len(expr)
        while i < n:
            ch = expr[i]
            if ch.isdigit() or ch == '.':
                # parse number
                num_str = ch
                i += 1
                while i < n and (expr[i].isdigit() or expr[i] == '.'):
                    num_str += expr[i]
                    i += 1
                try:
                    num = float(num_str)
                except ValueError:
                    return None
                operand_stack.append(num)
                continue  # already advanced i
            elif ch in self.operators:
                # handle operator precedence
                while (operator_stack and
                       self.precedence(ch) <= self.precedence(operator_stack[-1])):
                    operand_stack, operator_stack = self.apply_operator(
                        operand_stack, operator_stack)
                    if operand_stack is None:
                        return None
                operator_stack.append(ch)
            else:
                # invalid character
                return None
            i += 1

        # apply remaining operators
        while operator_stack:
            operand_stack, operator_stack = self.apply_operator(
                operand_stack, operator_stack)
            if operand_stack is None:
                return None

        if len(operand_stack) == 1:
            return operand_stack[0]
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
        if operator == '+':
            return 1
        if operator == '-':
            return 1
        if operator == '*':
            return 2
        if operator == '/':
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
        ([1, -1], ['-'])
        """
        if not operator_stack or len(operand_stack) < 2:
            return None, None
        op = operator_stack.pop()
        y = operand_stack.pop()
        x = operand_stack.pop()
        try:
            result = self.operators[op](x, y)
        except ZeroDivisionError:
            return None, None
        operand_stack.append(result)
        return operand_stack, operator_stack
