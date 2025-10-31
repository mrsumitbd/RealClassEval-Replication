from collections import defaultdict
from tabulate import tabulate

class AverageMeterDict:

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = defaultdict(int)
        self.avg = defaultdict(int)
        self.sum = defaultdict(int)
        self.count = defaultdict(int)

    def update(self, val, n=1):
        for k, v in val.items():
            self.val[k] = v
            self.count[k] += n
            self.sum[k] += v * n
            self.avg[k] = self.sum[k] / self.count[k]

    def message(self):
        msg = ''
        for k, v in self.avg.items():
            msg += f'{k}: {v.item():.4f}, '
        return msg.rstrip(', ')

    def message_verbose(self, sort=False):
        table_data = [{'Key': k, 'Value': f'{v.item():.4f}'} for k, v in self.avg.items()]
        if sort:
            table_data.sort(key=lambda x: x['Key'])
        return tabulate(table_data, headers='keys', tablefmt='pretty', numalign='center', stralign='left')