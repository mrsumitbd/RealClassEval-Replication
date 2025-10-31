class Counter:

    def __init__(self):
        self.next_value = 0

    def __next__(self):
        try:
            return self.next_value
        finally:
            self.next_value += 1

    def peek(self):
        return self.next_value