class MergeableStats:

    def __init__(self, ds_stats, ctx_stats):
        self.ds_stats = ds_stats
        self.ctx_stats = ctx_stats

    def __iter__(self):
        if self.ds_stats is not None:
            for x in self.ds_stats:
                yield from x.items()
        if self.ctx_stats is not None:
            yield from self.ctx_stats.items()