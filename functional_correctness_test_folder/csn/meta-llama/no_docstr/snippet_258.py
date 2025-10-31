
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
        data = np.array([self.fun(scale) for scale in scales])

        if part == 're':
            plt.plot(scales, np.real(data[key]))
        elif part == 'im':
            plt.plot(scales, np.imag(data[key]))
        elif part == 'abs':
            plt.plot(scales, np.abs(data[key]))
        elif part == 'all':
            plt.plot(scales, np.real(data[key]), label='Re')
            plt.plot(scales, np.imag(data[key]), label='Im')
            plt.legend()
        else:
            raise ValueError(
                "Invalid part. Choose from 're', 'im', 'abs', 'all'.")

        plt.xscale('log' if scale == 'log' else 'linear')
        plt.xlabel('Scale')
        plt.ylabel('Value')
        plt.title(f'{key} vs Scale')
        plt.show()
