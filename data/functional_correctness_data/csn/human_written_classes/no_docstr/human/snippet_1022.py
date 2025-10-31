import datetime

class ProcessingTask:

    def __init__(self):
        self.result = None
        self.id = 1
        self.time_create = datetime.datetime.now(datetime.timezone.utc)
        self.time_start = 0
        self.time_end = 0
        self.request = 'reduce'
        self.request_params = {}
        self.request_runinfo = self._init_runinfo()
        self.state = 0

    @classmethod
    def _init_runinfo(cls):
        request_runinfo = dict(runner='unknown', runner_version='unknown')
        return request_runinfo