import numpy as np

class WrappedBooster:

    def __init__(self, booster):
        self.booster_ = booster
        self.kwargs = _get_attributes(booster)
        if self.kwargs['num_class'] > 0:
            self.classes_ = self._generate_classes(self.kwargs)
            self.operator_name = 'XGBClassifier'
        else:
            self.operator_name = 'XGBRegressor'

    def get_xgb_params(self):
        return {k: v for k, v in self.kwargs.items() if v is not None}

    def get_booster(self):
        return self.booster_

    def _generate_classes(self, model_dict):
        if model_dict['num_class'] == 1:
            return np.asarray([0, 1])
        return np.arange(model_dict['num_class'])