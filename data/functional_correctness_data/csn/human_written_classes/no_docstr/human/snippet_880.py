class mirna:

    def __init__(self):
        self.p5 = 0
        self.p3 = 0

    def addp5(self, n, s, e):
        self.p5 = pos(n, s, e)

    def addp3(self, n, s, e):
        self.p3 = pos(n, s, e)