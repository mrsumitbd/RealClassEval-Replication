from skorch.utils import to_device
from torch.autograd import Variable
import torch

class Loader:

    def __init__(self, source, device='cpu', bptt=10, batch_size=20, evaluation=False):
        self.evaluation = evaluation
        self.bptt = bptt
        self.batch_size = batch_size
        self.device = device
        if isinstance(source.X, Variable):
            data = source.X.data.long()
        else:
            data = torch.LongTensor(source.X)
        self.batches = self.batchify(data, batch_size)

    def batchify(self, data, bsz):
        nbatch = data.size(0) // bsz
        data = data.narrow(0, 0, nbatch * bsz)
        data = data.view(bsz, -1).t().contiguous()
        return to_device(data, self.device)

    def get_batch(self, i):
        seq_len = min(self.bptt, len(self.batches) - 1 - i)
        data = Variable(self.batches[i:i + seq_len], volatile=self.evaluation)
        target = Variable(self.batches[i + 1:i + 1 + seq_len].view(-1))
        return (data, target)

    def __iter__(self):
        for i in range(0, self.batches.size(0) - 1, self.bptt):
            yield self.get_batch(i)