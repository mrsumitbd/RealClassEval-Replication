
import numpy as np


class RGsolution:

    def __init__(self, fun, scale_min, scale_max):
        self.fun = fun
        self.scale_min = scale_min
        self.scale_max = scale_max

    def plotdata(self, key, part='re', scale='log', steps=50):
        if scale == 'log':
            x = np.logspace(np.log10(self.scale_min),
                            np.log10(self.scale_max), steps)
        else:
            x = np.linspace(self.scale_min, self.scale_max, steps)
        y = []
        for xi in x:
            val = self.fun(xi)
            if isinstance(val, dict):
                v = val[key]
            else:
                v = getattr(val, key)
            if part == 're':
                y.append(np.real(v))
            elif part == 'im':
                y.append(np.imag(v))
            elif part == 'abs':
                y.append(np.abs(v))
            else:
                y.append(v)
        return x, np.array(y)
