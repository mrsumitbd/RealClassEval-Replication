
import numpy as np
import matplotlib.pyplot as plt


class RGsolution:

    def __init__(self, fun, scale_min, scale_max):
        self.fun = fun
        self.scale_min = scale_min
        self.scale_max = scale_max
        self.data = {}

    def plotdata(self, key, part='re', scale='log', steps=50):
        if key not in self.data:
            if scale == 'log':
                scales = np.logspace(self.scale_min, self.scale_max, steps)
            else:
                scales = np.linspace(self.scale_min, self.scale_max, steps)

            self.data[key] = [self.fun(s) for s in scales]

        data = np.array(self.data[key])
        scales = np.logspace(self.scale_min, self.scale_max, steps) if scale == 'log' else np.linspace(
            self.scale_min, self.scale_max, steps)

        if part == 're':
            plt.plot(scales, data.real)
        elif part == 'im':
            plt.plot(scales, data.imag)
        elif part == 'abs':
            plt.plot(scales, np.abs(data))
        elif part == 'arg':
            plt.plot(scales, np.angle(data))

        plt.xlabel('Scale')
        plt.ylabel('Value')
        plt.title(f'Plot of {key} for {part} part')
        plt.grid(True)
        plt.show()
