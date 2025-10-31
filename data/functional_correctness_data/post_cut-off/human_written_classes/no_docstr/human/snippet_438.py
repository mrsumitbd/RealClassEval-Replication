import dataclasses
import numpy as np

@dataclasses.dataclass
class DownscaleManager:
    base_shape: (list, tuple)
    scale_factor: (list, tuple)
    n_layers: (list, tuple)
    scale: (list, tuple) = None

    def __post_init__(self):
        ndim = len(self.base_shape)
        assert len(self.scale_factor) == ndim

    @property
    def _scale_ids(self):
        return np.arange(self.n_layers).reshape(-1, 1)

    @property
    def _theoretical_scale_factors(self):
        return np.power(self.scale_factor, self._scale_ids)

    @property
    def output_shapes(self):
        shapes = np.floor_divide(self.base_shape, self._theoretical_scale_factors)
        shapes[shapes == 0] = 1
        return shapes

    @property
    def scale_factors(self):
        return np.true_divide(self.output_shapes[0], self.output_shapes)

    @property
    def scales(self):
        return np.multiply(self.scale, self.scale_factors)