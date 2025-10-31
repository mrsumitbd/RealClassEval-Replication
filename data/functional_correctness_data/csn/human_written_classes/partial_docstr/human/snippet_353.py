class RunMonitor:
    """Track current runs and provide status.
    """

    def __init__(self):
        self._running = {}

    def set_status(self, run_id, status):
        self._running[run_id] = status

    def get_status(self, run_id):
        return self._running.get(run_id, 'not-running')