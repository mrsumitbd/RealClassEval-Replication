class RangeScaler:
    _data_min = None
    _data_scale = None
    _data_range = None

    def __init__(self, out_min, out_max):
        self._out_min = out_min
        self._out_scale = out_max - out_min

    def fit(self, X):
        data_max = X.max(axis=0)
        self._data_min = X.min(axis=0)
        self._data_scale = data_max - self._data_min
        self._data_range = (self._data_min, data_max)

    def scale(self, X):
        scaled = (X - self._data_min) / self._data_scale
        rescaled = scaled * self._out_scale + self._out_min
        return (rescaled, self._data_range)