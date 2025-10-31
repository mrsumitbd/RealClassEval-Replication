
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
        operand_stack = []
        operator_stack = []
        i = 0
        while i < len(expression):
            if expression[i].isdigit() or expression[i] == '.':
                j = i
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    i += 1
                operand_stack.append(float(expression[j:i]))
            elif expression[i] in self.operators:
                while (operator_stack and
                       self.precedence(operator_stack[-1]) >= self.precedence(expression[i])):
                    operand_stack, operator_stack = self.apply_operator(
                        operand_stack, operator_stack)
                operator_stack.append(expression[i])
                i += 1
            elif expression[i] == '(':
                operator_stack.append(expression[i])
                i += 1
            elif expression[i] == ')':
                while operator_stack[-1] != '(':
                    operand_stack, operator_stack = self.apply_operator(
                        operand_stack, operator_stack)
                operator_stack.pop()
                i += 1
            else:
                return None
        while operator_stack:
            if operator_stack[-1] == '(':
                return None
            operand_stack, operator_stack = self.apply_operator(
                operand_stack, operator_stack)
        return operand_stack[0]

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
        precedence_map = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '^': 3
        }
        return precedence_map.get(operator, 0)

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
        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()
        operator = operator_stack.pop()
        if operator in self.operators:
            result = self.operators[operator](operand1, operand2)
            operand_stack.append(result)
        return operand_stack, operator_stack
