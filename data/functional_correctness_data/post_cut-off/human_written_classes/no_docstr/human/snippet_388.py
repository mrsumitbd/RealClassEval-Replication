from random import randint

class Hmm:

    def __init__(self):
        self.value = randint(-100, 100)

    def Yeah(self):
        if self.value == 0:
            return True
        else:
            raise UhOh()