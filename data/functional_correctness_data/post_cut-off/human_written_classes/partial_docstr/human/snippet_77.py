import json

class BestMetricHolder:

    def __init__(self, init_res=0.0, better='large', use_ema=False) -> None:
        self.best_all = BestMetricSingle(init_res, better)
        self.use_ema = use_ema
        if use_ema:
            self.best_ema = BestMetricSingle(init_res, better)
            self.best_regular = BestMetricSingle(init_res, better)

    def update(self, new_res, epoch, is_ema=False):
        """
        return if the results is the best.
        """
        if not self.use_ema:
            return self.best_all.update(new_res, epoch)
        elif is_ema:
            self.best_ema.update(new_res, epoch)
            return self.best_all.update(new_res, epoch)
        else:
            self.best_regular.update(new_res, epoch)
            return self.best_all.update(new_res, epoch)

    def summary(self):
        if not self.use_ema:
            return self.best_all.summary()
        res = {}
        res.update({f'all_{k}': v for k, v in self.best_all.summary().items()})
        res.update({f'regular_{k}': v for k, v in self.best_regular.summary().items()})
        res.update({f'ema_{k}': v for k, v in self.best_ema.summary().items()})
        return res

    def __repr__(self) -> str:
        return json.dumps(self.summary(), indent=2)

    def __str__(self) -> str:
        return self.__repr__()