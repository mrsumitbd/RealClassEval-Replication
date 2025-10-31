class Notifier:

    def __init__(self, fun):
        self.fun = fun

    def notify(self, t):
        return not self.fun(t)