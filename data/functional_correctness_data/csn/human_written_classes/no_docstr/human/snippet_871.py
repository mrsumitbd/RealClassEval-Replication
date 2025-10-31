class RetryActionExecutor:

    def __init__(self, **kwds):
        raw_max_retries = kwds.get('max_retries', DEFAULT_MAX_RETRIES)
        self.max_retries = None if not raw_max_retries else int(raw_max_retries)
        self.interval_start = float(kwds.get('interval_start', DEFAULT_INTERVAL_START))
        self.interval_step = float(kwds.get('interval_step', DEFAULT_INTERVAL_STEP))
        self.interval_max = float(kwds.get('interval_max', DEFAULT_INTERVAL_MAX))
        self.errback = kwds.get('errback', self.__default_errback)
        self.catch = kwds.get('catch', DEFAULT_CATCH)
        self.default_description = kwds.get('description', DEFAULT_DESCRIPTION)

    def execute(self, action, description=None):

        def on_error(exc, intervals, retries, interval=0):
            interval = next(intervals)
            if self.errback:
                errback_args = [exc, interval]
                if description is not None:
                    errback_args.append(description)
                self.errback(exc, interval, description)
            return interval
        return _retry_over_time(action, catch=self.catch, max_retries=self.max_retries, interval_start=self.interval_start, interval_step=self.interval_step, interval_max=self.interval_max, errback=on_error)

    def __default_errback(self, exc, interval, description=None):
        description = description or self.default_description
        log.info('Failed to execute %s, retrying in %s seconds.', description, interval, exc_info=True)