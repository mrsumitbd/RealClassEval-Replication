
class Maximize:

    def __init__(self, guess):
        self.guess = guess
        self.best_guess = guess
        self.best_score = float('-inf')

    def __repr__(self):
        return f'Maximize(guess={self.best_guess})'
