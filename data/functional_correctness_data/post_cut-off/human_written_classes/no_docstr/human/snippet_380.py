class AverageMeterDict:

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = {}
        self.avg = {}
        self.sum = {}
        self.count = {}

    def update(self, val, n=1):
        for k, v in val.items():
            if k not in self.val:
                self.val[k] = 0
                self.sum[k] = 0
                self.count[k] = 0
            self.val[k] = v
            self.sum[k] += v * n
            self.count[k] += n
            self.avg[k] = self.sum[k] / self.count[k]