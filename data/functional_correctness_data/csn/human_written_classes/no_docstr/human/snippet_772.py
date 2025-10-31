import random

class StubProcess:

    def __init__(self, init_code=None, pid=None):
        self.shell = StubShell(init_code)
        self._identity = (pid,) if pid else (random.randint(0, int(1000000000000.0)),)

    def executeTask(self, task):
        return task(self.shell)