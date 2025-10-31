
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
            x = np.linspace(self.scale_min, self.scale_max, steps)
            y = self.fun(x)
            self.data[key] = {'x': x, 'y': y}

        x = self.data[key]['x']
        y = self.data[key]['y']

        if part == 're':
            y_part = np.real(y)
        elif part == 'im':
            y_part = np.imag(y)
        elif part == 'abs':
            y_part = np.abs(y)
        else:
            raise ValueError("part must be 're', 'im', or 'abs'")

        plt.figure()
        if scale == 'log':
            plt.loglog(x, y_part)
        elif scale == 'linear':
            plt.plot(x, y_part)
        else:
            raise ValueError("scale must be 'log' or 'linear'")

        plt.title(f'Plot of {part} part of {key}')
        plt.xlabel('x')
        plt.ylabel(part)
        plt.grid(True)
        plt.show()
