from typing import Optional

class DataIterator:

    def __init__(self, rollout_data, micro_batch_size: Optional[int]=None, micro_batch_indices: Optional[list[list[int]]]=None):
        self.rollout_data = rollout_data
        self.micro_batch_size = micro_batch_size
        self.micro_batch_indices = micro_batch_indices
        assert micro_batch_size is None or micro_batch_indices is None
        self.offset = 0

    def get_next(self, keys):
        batch = {}
        for key in keys:
            vals = self.rollout_data.get(key, None)
            if vals is None:
                batch[key] = None
            elif self.micro_batch_indices is not None:
                indices = self.micro_batch_indices[self.offset]
                batch[key] = [vals[i] for i in indices]
            else:
                assert self.offset + self.micro_batch_size <= len(vals), f'offset: {self.offset}, micro_batch_size: {self.micro_batch_size}, len(vals): {len(vals)}'
                batch[key] = vals[self.offset:self.offset + self.micro_batch_size]
        if self.micro_batch_indices is not None:
            self.offset += 1
        else:
            self.offset += self.micro_batch_size
        return batch

    def reset(self):
        self.offset = 0
        return self