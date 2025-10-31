class Canvas:

    def __init__(self, width, height, turtle=None):
        self.width = width
        self.height = height
        self.turtle = Turtle(0, 0, 0) if turtle is None else Turtle(*turtle)
        self.field = [[0 for i in range(width)] for j in range(height)]

    def put(self, s):
        for c in s:
            if c == '+':
                self.turtle.turn(1)
                continue
            if c == '-':
                self.turtle.turn(-1)
                continue
            if c == '[':
                self.turtle.push()
                continue
            if c == ']':
                self.turtle.pop()
                continue
            if c.isupper():
                w, h = (self.width, self.height)
                self.field[self.turtle.y % h][self.turtle.x % w] |= 1 << self.turtle.d
                self.turtle.move()
                self.field[self.turtle.y % h][self.turtle.x % w] |= 1 << (self.turtle.d + 2) % 4
                continue
            if c.islower():
                self.turtle.move()
        return self

    def render(self):
        chars = ' ─│╰──╯┴│╭│├╮┬┤┼'
        return list(map(lambda l: ''.join(map(lambda c: chars[c], l)), self.field))