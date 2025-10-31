
import random
import re
import ast
import operator
import math


class TwentyFourPointGame:
    """
    This ia a game of twenty-four points, which provides to generate four numbers and check whether player's expression is equal to 24.
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
        return list(self.nums)

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
        if not isinstance(expression, str) or not self.nums or len(self.nums) != 4:
            return False

        tokens = re.findall(r'\d+', expression)
        try:
            used_nums = list(map(int, tokens))
        except ValueError:
            return False

        if sorted(used_nums) != sorted(self.nums):
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
        if not isinstance(expression, str) or not expression.strip():
            return False

        try:
            node = ast.parse(expression, mode='eval')
            value = self._safe_eval(node.body)
            if not (isinstance(value, (int, float)) and math.isfinite(value)):
                return False
            return abs(value - 24) < 1e-6
        except Exception:
            return False

    def _safe_eval(self, node):
        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
        }

        if isinstance(node, ast.BinOp) and type(node.op) in ops:
            left = self._safe_eval(node.left)
            right = self._safe_eval(node.right)
            return ops[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            operand = self._safe_eval(node.operand)
            return +operand if isinstance(node.op, ast.UAdd) else -operand

        if isinstance(node, ast.Num):  # Python <3.8
            return node.n

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):  # Python 3.8+
            return node.value

        if isinstance(node, ast.Expression):
            return self._safe_eval(node.body)

        if isinstance(node, ast.Paren):
            return self._safe_eval(node.expr)

        if isinstance(node, ast.Call) or isinstance(node, ast.Name):
            raise ValueError("Not allowed")

        raise ValueError("Unsupported expression")
