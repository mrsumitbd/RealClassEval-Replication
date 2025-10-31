from typing import List, Iterable

class ContextualAutoTuner:
    _INSTANCE = None

    class KernelError(Exception):
        pass

    def __init__(self, fn, is_dist=False, n_repeat=5, n_warmup=3):
        self.fn = fn
        self.n_repeat = n_repeat
        self.n_warmup = n_warmup
        self.is_dist = is_dist
        self._ctxs: List[_TuningContext] = []
        self._log_file = dict()

    def dist_print(self, *args, **kwargs):
        import torch
        import os
        rank = torch.distributed.get_rank()
        file = self._log_file.get(rank, None)
        if file is None:
            os.makedirs('./.autotune_logs', exist_ok=True)
            file = open(f'./.autotune_logs/rank-{rank}.log', 'w')
            self._log_file[rank] = file
        print(f'[rank-{rank}]', *args, **kwargs, file=file, flush=True)

    def __call__(self, *args, **kwargs):

        def f_run():
            return self.fn(*args, **kwargs)
        assert ContextualAutoTuner._INSTANCE is None
        ContextualAutoTuner._INSTANCE = self
        self._ctxs = []
        try:
            while True:
                try:
                    ret = f_run()
                    break
                except self.KernelError:
                    continue
            if len(self._ctxs) <= 0:
                return ret
            while not all((ctx.finished for ctx in self._ctxs)):
                try:
                    f_run()
                except self.KernelError:
                    continue
            return f_run()
        finally:
            ContextualAutoTuner._INSTANCE = None
            self._ctxs = []