import pandas as pd

class SequentialMasker:

    def __init__(self, mask_type, sort_order, masker, model, *model_args, batch_size=500):
        for arg in model_args:
            if isinstance(arg, pd.DataFrame):
                raise TypeError('DataFrame arguments dont iterate correctly, pass numpy arrays instead!')
        self.inner = SequentialPerturbation(model, masker, sort_order, mask_type)
        self.model_args = model_args
        self.batch_size = batch_size

    def __call__(self, explanation, name, **kwargs):
        return self.inner(name, explanation, *self.model_args, batch_size=self.batch_size, **kwargs)