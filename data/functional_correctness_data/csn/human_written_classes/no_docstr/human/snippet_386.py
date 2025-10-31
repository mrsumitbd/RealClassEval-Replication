class Robot:

    def __init__(self):
        self.x = 0
        self.y = 0

    def __str__(self):
        return f'Robot position is {self.x}, {self.y}.'

    def interpret(self, model):
        for c in model.commands:
            if c.__class__.__name__ == 'InitialCommand':
                print(f'Setting position to: {c.x}, {c.y}')
                self.x = c.x
                self.y = c.y
            else:
                print(f'Going {c.direction} for {c.steps} step(s).')
                move = {'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'right': (1, 0)}[c.direction]
                self.x += c.steps * move[0]
                self.y += c.steps * move[1]
            print(self)