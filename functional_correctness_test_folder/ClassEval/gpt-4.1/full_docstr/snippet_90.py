
import random
import ast
import operator


class TwentyFourPointGame:
    """
    This is a game of twenty-four points, which provides to generate four numbers and check whether player's expression is equal to 24.
    """

    def __init__(self) -> None:
        self.nums = []

    def _generate_cards(self):
        """
        Generate random numbers between 1 and 9 for the cards.
        """
        self.nums = [random.randint(1, 9) for _ in range(4)]

    def get_my_cards(self):
        """
        Get a list of four random numbers between 1 and 9 representing the player's cards.
        :return: list of integers, representing the player's cards
        >>> game = TwentyFourPointGame()
        >>> game.get_my_cards()
        """
        self._generate_cards()
        return self.nums.copy()

    def answer(self, expression):
        """
        Check if a given mathematical expression using the cards can evaluate to 24.
        :param expression: string, mathematical expression using the cards
        :return: bool, True if the expression evaluates to 24, False otherwise
        >>> game = TwentyFourPointGame()
        >>> game.nums = [4, 3, 6, 6]
        >>> ans = "4*3+6+6"
        >>> ret = game.answer(ans)
        True
        """
        # Check if the expression uses exactly the numbers in self.nums
        try:
            nums_in_expr = self._extract_numbers(expression)
        except Exception:
            return False
        nums_sorted = sorted(self.nums)
        if sorted(nums_in_expr) != nums_sorted:
            return False
        return self.evaluate_expression(expression)

    def evaluate_expression(self, expression):
        """
        Evaluate a mathematical expression and check if the result is 24.
        :param expression: string, mathematical expression
        :return: bool, True if the expression evaluates to 24, False otherwise
        >>> game = TwentyFourPointGame()
        >>> nums = [4, 3, 6, 6]
        >>> ans = "4*3+6+6"
        >>> ret = game.evaluate_expression(ans)
        True
        """
        try:
            value = self._safe_eval(expression)
            return abs(value - 24) < 1e-6
        except Exception:
            return False

    def _extract_numbers(self, expression):
        """
        Extract all integer numbers from the expression as a list.
        """
        class NumberVisitor(ast.NodeVisitor):
            def __init__(self):
                self.nums = []

            def visit_Num(self, node):
                self.nums.append(node.n)

            def visit_Constant(self, node):
                if isinstance(node.value, int):
                    self.nums.append(node.value)
        tree = ast.parse(expression, mode='eval')
        visitor = NumberVisitor()
        visitor.visit(tree)
        return visitor.nums

    def _safe_eval(self, expr):
        """
        Safely evaluate a mathematical expression containing only numbers and +,-,*,/, parentheses.
        """
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
            ast.Pow: operator.pow,
        }

        def _eval(node):
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            elif isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                else:
                    raise ValueError("Invalid constant")
            elif isinstance(node, ast.BinOp):
                if type(node.op) not in allowed_operators:
                    raise ValueError("Operator not allowed")
                return allowed_operators[type(node.op)](_eval(node.left), _eval(node.right))
            elif isinstance(node, ast.UnaryOp):
                if type(node.op) not in allowed_operators:
                    raise ValueError("Operator not allowed")
                return allowed_operators[type(node.op)](_eval(node.operand))
            else:
                raise ValueError("Invalid expression")
        tree = ast.parse(expr, mode='eval')
        return _eval(tree)
