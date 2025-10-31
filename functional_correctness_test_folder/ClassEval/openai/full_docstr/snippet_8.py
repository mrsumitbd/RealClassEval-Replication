
class BalancedBrackets:
    """
    This is a class that checks for bracket matching
    """

    def __init__(self, expr):
        """
        Initializes the class with an expression.
        :param expr: The expression to check for balanced brackets,str.
        """
        self.stack = []
        self.left_brackets = ["(", "{", "["]
        self.right_brackets = [")", "}", "]"]
        self.expr = expr

    def clear_expr(self):
        """
        Clears the expression of all characters that are not brackets.
        >>> b = BalancedBrackets("a(b)c")
        >>> b.clear_expr()
        >>> b.expr
        '()'
        """
        # Keep only characters that are in left or right brackets
        self.expr = "".join(
            ch for ch in self.expr if ch in self.left_brackets + self.right_brackets)

    def check_balanced_brackets(self):
        """
        Checks if the expression has balanced brackets.
        :return: True if the expression has balanced brackets, False otherwise.
        >>> b = BalancedBrackets("a(b)c")
        >>> b.check_balanced_brackets()
        True
        """
        # Ensure expression contains only brackets
        self.clear_expr()
        # Reset stack
        self.stack = []

        for ch in self.expr:
            if ch in self.left_brackets:
                self.stack.append(ch)
            elif ch in self.right_brackets:
                if not self.stack:
                    return False
                last_left = self.stack.pop()
                # Check if the popped left bracket matches the current right bracket
                if self.left_brackets.index(last_left) != self.right_brackets.index(ch):
                    return False
        # If stack is empty, all brackets matched
        return not self.stack
