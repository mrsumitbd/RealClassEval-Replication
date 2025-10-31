from modopt.base.backend import get_array_module, get_backend

class PowerMethod:
    """Power method class.

    This method performs implements power method to calculate the spectral
    radius of the input data.

    Parameters
    ----------
    operator : callable
        Operator function
    data_shape : tuple
        Shape of the data array
    data_type : {``float``, ``complex``}, optional
        Random data type (default is ``float``)
    auto_run : bool, optional
        Option to automatically calcualte the spectral radius upon
        initialisation (default is ``True``)
    verbose : bool, optional
        Optional verbosity (default is ``False``)
    rng: int, xp.random.Generator or None (default is ``None``)
        Random number generator or seed.

    Examples
    --------
    >>> import numpy as np
    >>> from modopt.math.matrix import PowerMethod
    >>> np.random.seed(1)
    >>> pm = PowerMethod(lambda x: x.dot(x.T), (3, 3))
    >>> np.around(pm.spec_rad, 6)
    1.0
    >>> np.around(pm.inv_spec_rad, 6)
    1.0

    Notes
    -----
    Implementation from: https://en.wikipedia.org/wiki/Power_iteration

    """

    def __init__(self, operator, data_shape, data_type=float, auto_run=True, compute_backend='numpy', verbose=False, rng=None):
        self._operator = operator
        self._data_shape = data_shape
        self._data_type = data_type
        self._verbose = verbose
        xp, compute_backend = get_backend(compute_backend)
        self.xp = xp
        self.rng = None
        self.compute_backend = compute_backend
        if auto_run:
            self.get_spec_rad()

    def _set_initial_x(self):
        """Set initial value of :math:`x`.

        This method sets the initial value of :math:`x` to an arrray of random
        values.

        Returns
        -------
        numpy.ndarray
            Random values of the same shape as the input data

        """
        rng = self.xp.random.default_rng(self.rng)
        return rng.random(self._data_shape).astype(self._data_type)

    def get_spec_rad(self, tolerance=1e-06, max_iter=20, extra_factor=1.0):
        """Get spectral radius.

        This method calculates the spectral radius

        Parameters
        ----------
        tolerance : float, optional
            Tolerance threshold for convergence (default is ``1e-6``)
        max_iter : int, optional
            Maximum number of iterations (default is ``20``)
        extra_factor : float, optional
            Extra multiplicative factor for calculating the spectral radius
            (default is ``1.0``)

        """
        x_old = self._set_initial_x()
        xp = get_array_module(x_old)
        x_old_norm = xp.linalg.norm(x_old)
        x_old /= x_old_norm
        for i_elem in range(max_iter):
            xp = get_array_module(x_old)
            x_new = self._operator(x_old)
            x_new_norm = xp.linalg.norm(x_new)
            x_new /= x_new_norm
            if xp.abs(x_new_norm - x_old_norm) < tolerance:
                message = ' - Power Method converged after {0} iterations!'
                if self._verbose:
                    print(message.format(i_elem + 1))
                break
            elif i_elem == max_iter - 1 and self._verbose:
                message = ' - Power Method did not converge after {0} iterations!'
                print(message.format(max_iter))
            xp.copyto(x_old, x_new)
            x_old_norm = x_new_norm
        self.spec_rad = x_new_norm * extra_factor
        self.inv_spec_rad = 1.0 / self.spec_rad