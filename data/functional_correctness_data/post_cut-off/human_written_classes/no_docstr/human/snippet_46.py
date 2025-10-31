class BestMetricSingle:

    def __init__(self, init_res=0.0, better='large') -> None:
        self.init_res = init_res
        self.best_res = init_res
        self.best_ep = -1
        self.better = better
        assert better in ['large', 'small']

    def isbetter(self, new_res, old_res):
        if self.better == 'large':
            return new_res > old_res
        if self.better == 'small':
            return new_res < old_res

    def update(self, new_res, ep):
        if self.isbetter(new_res, self.best_res):
            self.best_res = new_res
            self.best_ep = ep
            return True
        return False

    def __str__(self) -> str:
        return 'best_res: {}\t best_ep: {}'.format(self.best_res, self.best_ep)

    def __repr__(self) -> str:
        return self.__str__()

    def summary(self) -> dict:
        return {'best_res': self.best_res, 'best_ep': self.best_ep}