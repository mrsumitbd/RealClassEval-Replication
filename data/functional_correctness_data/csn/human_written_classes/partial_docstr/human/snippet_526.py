class Collector:
    """Base class for collectors.

    To subclass `Collector`:

    * implement method `fetch(self, smc)` which computes the summary that
      must be collected (from object smc, at each time).
    * (optionally) define class attribute `summary_name` (name of the collected summary;
      by default, name of the class, un-capitalised, i.e. Moments > moments)
    * (optionally) define class attribute `signature` (the signature of the
      constructor, by default, an empty dict)
    """
    signature = {}

    @property
    def summary_name(self):
        cn = self.__class__.__name__
        return cn[0].lower() + cn[1:]

    def __init__(self, **kwargs):
        self.summary = []
        for k, v in self.signature.items():
            setattr(self, k, v)
        for k, v in kwargs.items():
            if k in self.signature.keys():
                setattr(self, k, v)
            else:
                raise ValueError(f'Collector {self.__class__.__name__}: unknown parameter {k}')

    def __call__(self):
        return self.__class__(**{k: getattr(self, k) for k in self.signature.keys()})

    def collect(self, smc):
        self.summary.append(self.fetch(smc))