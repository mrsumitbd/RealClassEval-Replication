import numpy as np
from math import log, e

class RGsolution:
    """Class representing a continuous (interpolated) solution to the
    SMEFT RGEs to be used for plotting."""

    def __init__(self, fun, scale_min, scale_max):
        """Initialize.

        Parameters:

        - fun: function of the scale that is expected to return a
        dictionary with the RGE solution and to accept vectorized input.
        - scale_min, scale_max: lower and upper boundaries of the scale
        """
        self.fun = fun
        self.scale_min = scale_min
        self.scale_max = scale_max

    def plotdata(self, key, part='re', scale='log', steps=50):
        """Return a tuple of arrays x, y that can be fed to plt.plot,
        where x is the scale in GeV and y is the parameter of interest.

        Parameters:

        - key: dicionary key of the parameter to be plotted (e.g. a WCxf
          coefficient name or a SM parameter like 'g')
        - part: plot the real part 're' (default) or the imaginary part 'im'
        - scale: 'log'; make the x steps logarithmically distributed; for
          'linear', linearly distributed
        - steps: steps in x to take (default: 50)
        """
        if scale == 'log':
            x = np.logspace(log(self.scale_min), log(self.scale_max), steps, base=e)
        elif scale == 'linear':
            x = np.linspace(self.scale_min, self.scale_max, steps)
        y = self.fun(x)
        y = np.array([d[key] for d in y])
        if part == 're':
            return (x, y.real)
        elif part == 'im':
            return (x, y.imag)

    def plot(self, key, part='re', scale='log', steps=50, legend=True, plotargs={}):
        """Plot the RG evolution of parameter `key`.

        Parameters:

        - part, scale, steps: see `plotdata`
        - legend: boolean, show the legend (default: True)
        - plotargs: dictionary of arguments to be passed to plt.plot
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError('Please install matplotlib if you want to use the plot method')
        pdat = self.plotdata(key, part=part, scale=scale, steps=steps)
        plt.plot(*pdat, label=key, **plotargs)
        if scale == 'log':
            plt.xscale('log')
        if legend:
            plt.legend()