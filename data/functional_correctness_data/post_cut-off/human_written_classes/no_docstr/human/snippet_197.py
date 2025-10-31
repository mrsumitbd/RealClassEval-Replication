from imaginaire.utils import distributed, log

class TeroPolyScheduler:

    def __init__(self, total_Mimg: int, batch_size: int, ref_Mimg: int | None=None, ref_batches: float=70000.0 / 1024, max_lr_ratio: float | None=1.0, min_lr_ratio: float | None=None, rampup_Mimg: float=0, rampdown_Mimg: int=0, verbosity_interval: int=0, formula: str='poly', poly_exp: float=0.5):
        self.total_Mimg = total_Mimg
        self.batch_size = batch_size * distributed.get_world_size()
        self.ref_Mimg = ref_Mimg or ref_batches * batch_size / 1000000.0
        self.ref_batches = ref_batches
        self.max_lr_ratio = max_lr_ratio
        self.min_lr_ratio = min_lr_ratio
        self.rampup_Mimg = rampup_Mimg
        self.rampdown_Mimg = rampdown_Mimg
        self.verbosity_interval = verbosity_interval
        self.formula = formula
        self.poly_exp = poly_exp
        self._model = None

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    def schedule(self, n, **kwargs):
        cur_Mimg = getattr(self.model, 'sample_counter', 0) / 1000000.0
        if self.formula == 'constant':
            lr = 1.0
        elif self.formula == 'poly':
            lr = max(cur_Mimg / self.ref_Mimg, 1e-08) ** (-self.poly_exp)
        else:
            raise ValueError(f'Invalid learning rate formula "{self.formula}"')
        if self.max_lr_ratio is not None:
            lr = min(lr, self.max_lr_ratio)
        if self.min_lr_ratio is not None:
            lr = max(lr, self.min_lr_ratio)
        if self.rampup_Mimg > 0 and cur_Mimg < self.rampup_Mimg:
            lr *= cur_Mimg / self.rampup_Mimg
        if self.rampdown_Mimg > 0 and cur_Mimg > self.total_Mimg - self.rampdown_Mimg:
            lr *= (self.total_Mimg - cur_Mimg) / self.rampdown_Mimg
        return lr

    def __call__(self, n, **kwargs):
        return self.schedule(n, **kwargs)