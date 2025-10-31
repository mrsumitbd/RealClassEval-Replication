class Comment:

    def __init__(self, line):
        self.line = line

    def __str__(self):
        if self.line.startswith('#'):
            return self.line
        return '#' + self.line