import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from typing import Any, Callable, Iterable, List, Tuple, Union, cast

class KrigingObject:
    """Interpolation function like object for Kriging"""

    def __init__(self, times: np.ndarray, series: np.ndarray, **kwargs: Any):
        self.regressor = GaussianProcessRegressor(**kwargs)
        self.normalizing_factor = max(times) - min(times)
        self.regressor.fit(times.reshape(-1, 1) / self.normalizing_factor, series)
        self.call_args = kwargs.get('call_args', {})

    def __call__(self, new_times: np.ndarray, **kwargs: Any) -> np.ndarray:
        call_args = self.call_args.copy()
        call_args.update(kwargs)
        return self.regressor.predict(new_times.reshape(-1, 1) / self.normalizing_factor, **call_args)