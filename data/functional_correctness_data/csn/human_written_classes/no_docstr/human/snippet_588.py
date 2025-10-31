class World:

    def __init__(self):
        self.s = 'Hello'

    def tick(self):
        self.s += '|'
        self.s = self.s[max(1, len(self.s) - 80):]

    def process_event(self, e):
        self.s += str(e)