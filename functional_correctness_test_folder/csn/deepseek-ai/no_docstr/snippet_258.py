
import numpy as np
import matplotlib.pyplot as plt


class RGsolution:

    def __init__(self, fun, scale_min, scale_max):
        self.fun = fun
        self.scale_min = scale_min
        self.scale_max = scale_max

    def plotdata(self, key, part='re', scale='log', steps=50):
        scales = np.logspace(np.log10(self.scale_min), np.log10(
            self.scale_max), steps) if scale == 'log' else np.linspace(self.scale_min, self.scale_max, steps)
        values = []
        for s in scales:
            val = self.fun(s, key)
            if part == 're':
                values.append(np.real(val))
            elif part == 'im':
                values.append(np.imag(val))
            elif part == 'abs':
                values.append(np.abs(val))
            else:
                raise ValueError("part must be 're', 'im', or 'abs'")

        plt.figure()
        if scale == 'log':
            plt.loglog(scales, values)
        else:
            plt.plot(scales, values)
        plt.xlabel('Scale')
        plt.ylabel(part)
        plt.title(f'{part} part of {key}')
        plt.grid(True)
        plt.show()
