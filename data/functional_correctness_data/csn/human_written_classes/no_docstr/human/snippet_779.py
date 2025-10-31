class RangeUnscaler:

    def __init__(self, out_min, out_max):
        self._out_min = out_min
        self._out_scale = out_max - out_min

    def fit(self, data_range):
        self._data_min = data_range[0]
        self._data_scale = data_range[1] - self._data_min

    def unscale(self, X):
        unscaled = (X - self._out_min) / self._out_scale
        return unscaled * self._data_scale + self._data_min