
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
        try:
            tokens = self.tokenize(expression)
            operand_stack = []
            operator_stack = []

            i = 0
            while i < len(tokens):
                token = tokens[i]
                if self.is_number(token):
                    operand_stack.append(float(token))
                elif token in self.operators:
                    while (operator_stack and
                           self.precedence(operator_stack[-1]) >= self.precedence(token)):
                        operand_stack, operator_stack = self.apply_operator(
                            operand_stack, operator_stack)
                    operator_stack.append(token)
                i += 1

            while operator_stack:
                operand_stack, operator_stack = self.apply_operator(
                    operand_stack, operator_stack)

            if len(operand_stack) == 1:
                return operand_stack[0]
            else:
                return None
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
        priorities = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        return priorities.get(operator, 0)

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
        if len(operand_stack) < 2 or not operator_stack:
            return operand_stack, operator_stack
        right = operand_stack.pop()
        left = operand_stack.pop()
        op = operator_stack.pop()
        result = self.operators[op](left, right)
        operand_stack.append(result)
        return operand_stack, operator_stack

    def is_number(self, s):
        try:
            float(s)
            return True
        except:
            return False

    def tokenize(self, expr):
        tokens = []
        i = 0
        n = len(expr)
        while i < n:
            if expr[i].isspace():
                i += 1
                continue
            if expr[i] in self.operators:
                tokens.append(expr[i])
                i += 1
            elif expr[i].isdigit() or expr[i] == '.':
                num = []
                dot_count = 0
                while i < n and (expr[i].isdigit() or expr[i] == '.'):
                    if expr[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            break
                    num.append(expr[i])
                    i += 1
                tokens.append(''.join(num))
            else:
                # Invalid character
                return []
        return tokens
