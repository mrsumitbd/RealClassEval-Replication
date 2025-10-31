
class Minimize:

    def __init__(self, guess):
        self.value = min(guess)

    def __repr__(self):
        return f"Minimize({self.value})"
