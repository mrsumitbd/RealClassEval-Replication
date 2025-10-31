
import random


class TwentyFourPointGame:
    """
    This is a game of twenty-four points, which provides to generate four numbers and check whether player's expression is equal to 24.
    """

    def __init__(self) -> None:
        self.nums = []
        self._generate_cards()

    def _generate_cards(self):
        """
        Generate random numbers between 1 and 9 for the cards.
        """
        self.nums = random.choices(range(1, 10), k=4)

    def get_my_cards(self):
        """
        Get a list of four random numbers between 1 and 9 representing the player's cards.
        :return: list of integers, representing the player's cards
        >>> game = TwentyFourPointGame()
        >>> game.get_my_cards()

        """
        return self.nums

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
        for i, num in enumerate(self.nums):
            expression = expression.replace(str(i+1), str(num))
        try:
            return self.evaluate_expression(expression)
        except Exception:
            return False

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
            result = eval(expression)
            return abs(result - 24) < 1e-6
        except Exception:
            return False


# Example usage:
if __name__ == "__main__":
    game = TwentyFourPointGame()
    print("Your cards are: ", game.get_my_cards())
    expression = input(
        "Enter your expression (using 1, 2, 3, 4 to represent the cards): ")
    print("Is your expression correct? ", game.answer(expression))
