
import numpy as np
import matplotlib.pyplot as plt


class RGsolution:
    '''Class representing a continuous (interpolated) solution to the
    SMEFT RGEs to be used for plotting.'''

    def __init__(self, fun, scale_min, scale_max):
        '''Initialize.
        Parameters:
        - fun: function of the scale that is expected to return a
        dictionary with the RGE solution and to accept vectorized input.
        - scale_min, scale_max: lower and upper boundaries of the scale
        '''
        self.fun = fun
        self.scale_min = scale_min
        self.scale_max = scale_max

    def plotdata(self, key, part='re', scale='log', steps=50):
        '''Return a tuple of arrays x, y that can be fed to plt.plot,
        where x is the scale in GeV and y is the parameter of interest.
        Parameters:
        - key: dicionary key of the parameter to be plotted (e.g. a WCxf
          coefficient name or a SM parameter like 'g')
        - part: plot the real part 're' (default) or the imaginary part 'im'
        - scale: 'log'; make the x steps logarithmically distributed; for
          'linear', linearly distributed
        - steps: steps in x to take (default: 50)
        '''
        if scale == 'log':
            x = np.logspace(np.log10(self.scale_min),
                            np.log10(self.scale_max), steps)
        elif scale == 'linear':
            x = np.linspace(self.scale_min, self.scale_max, steps)
        else:
            raise ValueError("Invalid scale. Use 'log' or 'linear'.")

        y_dict = self.fun(x)
        y = y_dict[key]

        if part == 're':
            y = np.real(y)
        elif part == 'im':
            y = np.imag(y)
        else:
            raise ValueError("Invalid part. Use 're' or 'im'.")

        return x, y

    def plot(self, key, part='re', scale='log', steps=50, legend=True, plotargs=None):
        '''Plot the RG evolution of parameter `key`.
        Parameters:
        - part, scale, steps: see `plotdata`
        - legend: boolean, show the legend (default: True)
        - plotargs: dictionary of arguments to be passed to plt.plot
        '''
        x, y = self.plotdata(key, part, scale, steps)

        if plotargs is None:
            plotargs = {}

        plt.plot(x, y, label=key, **plotargs)

        if legend:
            plt.legend()

        plt.xlabel('Scale [GeV]')
        plt.ylabel(key)
        plt.xscale(scale)
        plt.grid(True)
