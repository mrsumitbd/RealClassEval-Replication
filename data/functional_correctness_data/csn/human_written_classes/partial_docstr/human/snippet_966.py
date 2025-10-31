class Search:
    """A user-created search object.

    Used to prepare a :class:`~bloop.search.PreparedSearch` which build search iterators.

    :param str mode: Search type, either "query" or "scan".
    :param engine: :class:`~bloop.engine.Engine` to unpack models with.
    :param model: :class:`~bloop.models.BaseModel` being searched.
    :param index: :class:`~bloop.models.Index` to search, or None.
    :param key: *(Query only)* Key condition.  This must include an equality against the hash key,
        and optionally one of a restricted set of conditions on the range key.
    :param filter: Filter condition.  Only matching objects will be included in the results.
    :param projection: "all", "count", a set of column names, or a list of :class:`~bloop.models.Column`.
        When projection is "count", you must advance the iterator to retrieve the count.
    :param bool consistent: Use `strongly consistent reads`__ if True.  Not applicable to GSIs.  Default is False.
    :param bool forward: *(Query only)* Use ascending or descending order.  Default is True (ascending).
    :param tuple parallel: *(Scan only)* A tuple of (Segment, TotalSegments) for this portion of a `parallel scan`__.
            Default is None.

    __ http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html
    __ http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/QueryAndScan.html#QueryAndScanParallelScan
    """

    def __init__(self, mode=None, engine=None, model=None, index=None, key=None, filter=None, projection=None, consistent=False, forward=True, parallel=None):
        self.mode = mode
        self.engine = engine
        self.model = model
        self.index = index
        self.key = key
        self.filter = filter
        self.projection = projection
        self.consistent = consistent
        self.forward = forward
        self.parallel = parallel

    def __repr__(self):
        return search_repr(self.__class__, self.model, self.index)

    def prepare(self):
        """Constructs a :class:`~bloop.search.PreparedSearch`."""
        p = PreparedSearch()
        p.prepare(engine=self.engine, mode=self.mode, model=self.model, index=self.index, key=self.key, filter=self.filter, projection=self.projection, consistent=self.consistent, forward=self.forward, parallel=self.parallel)
        return p