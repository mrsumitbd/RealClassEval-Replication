
class Minimize:

    def __init__(self, guess):
        self.guess = guess
        self.iterations = 0

    def __repr__(self):
        return f"Minimize(guess={self.guess}, iterations={self.iterations})"
