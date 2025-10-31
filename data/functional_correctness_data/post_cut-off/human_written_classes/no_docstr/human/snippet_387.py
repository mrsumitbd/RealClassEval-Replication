from collections import defaultdict

class AverageMeterDictList:

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = defaultdict(list)
        self.avg = defaultdict(list)
        self.sum = defaultdict(list)
        self.count = defaultdict(int)

    def update(self, val, n=1):
        for k, v in val.items():
            self.val[k] = v
            self.count[k] += n
            assert isinstance(v, list), 'Error: values of this meter should be a list'
            last_len = len(self.sum[k])
            if last_len == 0:
                self.sum[k] = [0.0] * len(v)
                self.avg[k] = [0.0] * len(v)
            else:
                assert last_len == len(v), f'Error: list length of {k} mismatch.'
            for i in range(len(v)):
                self.sum[k][i] += v[i] * n
                self.avg[k][i] = self.sum[k][i] / self.count[k]

    def message(self):
        msg = ''
        for k, v in self.avg.items():
            formatted_values = ','.join([f'{x.item():.4f}' for x in v])
            msg += f'{k}: {formatted_values}, '
        return msg.rstrip(', ')