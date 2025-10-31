
import numpy as np
import matplotlib.pyplot as plt


class RGsolution:
    def __init__(self, fun, scale_min, scale_max):
        """
        Parameters
        ----------
        fun : callable
            Function that takes a scale value and returns either a scalar,
            a complex number, or a dictionary/array of values.
        scale_min : float
            Minimum scale value.
        scale_max : float
            Maximum scale value.
        """
        self.fun = fun
        self.scale_min = scale_min
        self.scale_max = scale_max

    def plotdata(self, key, part='re', scale='log', steps=50):
        """
        Plot the data returned by `fun` over the specified scale range.

        Parameters
        ----------
        key : str or int or None
            If the output of `fun` is a dict or array, this selects the
            element to plot. If None, the entire output is plotted.
        part : {'re', 'im', 'abs', 'phase'}, optional
            Which part of the data to plot. Default is 're'.
        scale : {'log', 'linear'}, optional
            Scale of the x-axis. Default is 'log'.
        steps : int, optional
            Number of points in the scale grid. Default is 50.
        """
        # Generate scale values
        if scale == 'log':
            scales = np.logspace(np.log10(self.scale_min),
                                 np.log10(self.scale_max), steps)
        else:
            scales = np.linspace(self.scale_min, self.scale_max, steps)

        # Evaluate the function
        values = []
        for s in scales:
            val = self.fun(s)
            # If val is a dict or array, extract the requested key/element
            if isinstance(val, dict):
                if key is None:
                    raise ValueError(
                        "Key must be specified for dictionary output.")
                val = val[key]
            elif isinstance(val, (list, tuple, np.ndarray)):
                if key is None:
                    raise ValueError(
                        "Key must be specified for array/list output.")
                val = val[key]
            values.append(val)

        values = np.array(values)

        # Select part of the data
        if np.iscomplexobj(values):
            if part == 're':
                plot_vals = np.real(values)
            elif part == 'im':
                plot_vals = np.imag(values)
            elif part == 'abs':
                plot_vals = np.abs(values)
            elif part == 'phase':
                plot_vals = np.angle(values)
            else:
                raise ValueError(f"Unknown part '{part}'.")
        else:
            plot_vals = values

        # Plot
        plt.figure(figsize=(8, 5))
        plt.plot(scales, plot_vals, marker='o', linestyle='-')
        plt.xscale(scale)
        plt.xlabel('Scale')
        plt.ylabel(f'{key} ({part})')
        plt.title(f'Plot of {key} vs Scale')
        plt.grid(True, which='both', ls='--', lw=0.5)
        plt.tight_layout()
        plt.show()
