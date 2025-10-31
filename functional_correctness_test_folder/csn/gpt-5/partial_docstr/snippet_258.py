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
        if scale_min <= 0 or scale_max <= 0:
            raise ValueError(
                "scale_min and scale_max must be positive for log scaling.")
        if scale_min >= scale_max:
            raise ValueError("scale_min must be smaller than scale_max.")
        if not callable(fun):
            raise TypeError("fun must be callable.")
        self.fun = fun
        self.scale_min = float(scale_min)
        self.scale_max = float(scale_max)

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
        if steps < 2:
            raise ValueError("steps must be >= 2.")
        if scale not in ('log', 'linear'):
            raise ValueError("scale must be 'log' or 'linear'.")
        if part not in ('re', 'im'):
            raise ValueError("part must be 're' or 'im'.")

        if scale == 'log':
            x = np.logspace(np.log10(self.scale_min),
                            np.log10(self.scale_max), steps)
        else:
            x = np.linspace(self.scale_min, self.scale_max, steps)

        try:
            out = self.fun(x)
        except Exception:
            # Fallback to non-vectorized evaluation
            vals = []
            for xi in x:
                d = self.fun(float(xi))
                if key not in d:
                    raise KeyError(
                        f"Key '{key}' not found in solution dictionary.")
                vals.append(d[key])
            y = np.asarray(vals)
        else:
            if key not in out:
                raise KeyError(
                    f"Key '{key}' not found in solution dictionary.")
            y = np.asarray(out[key])

        # Ensure y is 1D aligned with x
        y = np.squeeze(y)
        if y.shape != x.shape:
            # Attempt broadcasting if possible
            try:
                y = np.broadcast_to(y, x.shape)
            except Exception:
                raise ValueError(
                    f"Shape of y {y.shape} is incompatible with x {x.shape}.")

        # Select part
        if np.iscomplexobj(y):
            y = np.real(y) if part == 're' else np.imag(y)
        else:
            if part == 'im':
                y = np.zeros_like(y, dtype=float)
            else:
                y = y.astype(float)

        return x, y

    def plot(self, key, part='re', scale='log', steps=50, legend=True, plotargs=None, label=None):
        '''Plot the RG evolution of parameter `key`.
        Parameters:
        - part, scale, steps: see `plotdata`
        - legend: boolean, show the legend (default: True)
        - plotargs: dictionary of arguments to be passed to plt.plot
        '''
        x, y = self.plotdata(key, part=part, scale=scale, steps=steps)
        if plotargs is None:
            plotargs = {}
        if label is None:
            label = f"{key} ({part})"
        line, = plt.plot(x, y, label=label, **plotargs)
        if scale == 'log':
            plt.xscale('log')
        plt.xlabel("Scale [GeV]")
        plt.ylabel(key)
        if legend:
            plt.legend()
        return line
