import numpy as np


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
        if not callable(fun):
            raise TypeError("fun must be callable")
        try:
            smin = float(scale_min)
            smax = float(scale_max)
        except Exception as e:
            raise TypeError("scale_min and scale_max must be numeric") from e
        if not np.isfinite(smin) or not np.isfinite(smax):
            raise ValueError("scale_min and scale_max must be finite numbers")
        if smax <= smin:
            raise ValueError("scale_max must be greater than scale_min")

        self.fun = fun
        self.scale_min = smin
        self.scale_max = smax

    def _compute_xy(self, key, part='re', scale='log', steps=50):
        if part not in ('re', 'im'):
            raise ValueError("part must be 're' or 'im'")
        if scale not in ('log', 'linear'):
            raise ValueError("scale must be 'log' or 'linear'")
        try:
            steps = int(steps)
        except Exception as e:
            raise TypeError("steps must be an integer") from e
        if steps < 2:
            raise ValueError("steps must be at least 2")

        if scale == 'log':
            if self.scale_min <= 0 or self.scale_max <= 0:
                raise ValueError(
                    "Log scale requires positive scale_min and scale_max")
            x = np.logspace(np.log10(self.scale_min),
                            np.log10(self.scale_max), steps)
        else:
            x = np.linspace(self.scale_min, self.scale_max, steps)

        res = self.fun(x)
        if not isinstance(res, dict):
            raise TypeError("fun must return a dictionary")
        if key not in res:
            raise KeyError(f"Key '{key}' not found in fun(x) result")
        y = np.asarray(res[key])

        # Support broadcasting scalar outputs or 1D arrays aligned with x
        if y.shape == ():
            y = np.full_like(
                x, fill_value=y, dtype=np.result_type(y, np.float64))
        elif y.shape != x.shape:
            try:
                y = np.broadcast_to(y, x.shape)
            except Exception:
                raise ValueError(
                    f"Output for key '{key}' has incompatible shape {y.shape}; expected broadcastable to {x.shape}")

        if np.iscomplexobj(y):
            y = np.real(y) if part == 're' else np.imag(y)
        else:
            if part == 'im':
                # real input; imaginary part is zero
                y = np.zeros_like(x, dtype=float)

        y = np.asarray(y, dtype=float)
        return x, y

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
        return self._compute_xy(key=key, part=part, scale=scale, steps=steps)

    def plotdata(self, key, part='re', scale='log', steps=50):
        '''Plot the RG evolution of parameter `key`.
        Parameters:
        - part, scale, steps: see `plotdata`
        - legend: boolean, show the legend (default: True)
        - plotargs: dictionary of arguments to be passed to plt.plot
        '''
        # Despite the docstring, this method returns data suitable for plotting.
        # The signature provided does not allow passing plotting kwargs here.
        return self._compute_xy(key=key, part=part, scale=scale, steps=steps)
