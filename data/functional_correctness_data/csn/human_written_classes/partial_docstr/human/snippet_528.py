class Summaries:
    """Class to store and update summaries.

    Attribute ``summaries`` of ``SMC`` objects is an instance of this class.
    """

    def __init__(self, cols):
        self._collectors = [cls() for cls in default_collector_cls]
        if cols is not None:
            self._collectors.extend((col() for col in cols))
        for col in self._collectors:
            setattr(self, col.summary_name, col.summary)

    def collect(self, smc):
        for col in self._collectors:
            col.collect(smc)