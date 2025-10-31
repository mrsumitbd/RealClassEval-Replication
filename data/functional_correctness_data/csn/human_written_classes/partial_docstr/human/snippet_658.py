class Runner:
    """
    This runner class takea a generator function and run it.
    1. When the generator returns None, continue to run without yielding.
    2. When the generator returns a poller, continue is it receives any message in 0.2s.
    3. Otherwise return False.
    4. The the generator completes, return True.

    So in summary, the Runner returns
    1. True if all completed, return value from generator is ignored.
    2. `self` if waiting.
    """

    def __init__(self, runner, name):
        self._runner = runner
        self._poller = 0
        self._name = name

    def __repr__(self):
        return self._name

    def run_until_waiting(self):
        try:
            if self._poller == 0:
                self._poller = next(self._runner)
            while True:
                if self._poller is None:
                    self._poller = self._runner.send(None)
                    continue
                if self._poller.poll(200):
                    self._poller = self._runner.send(None)
                    continue
                return self
        except StopIteration:
            return True

    def can_proceed(self):
        return self._poller.poll(0)