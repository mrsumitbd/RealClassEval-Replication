
class Maximize:

    def __init__(self, guess):
        self.guess = guess

    def __repr__(self):
        if isinstance(self.guess, (list, tuple)):
            try:
                max_val = max(self.guess)
            except ValueError:
                return "Maximize(empty)"
            return f"Maximize({max_val})"
        else:
            return f"Maximize({self.guess})"
