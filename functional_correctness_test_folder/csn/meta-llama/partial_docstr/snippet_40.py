
import matplotlib
from IPython import get_ipython


class interactive_backend:
    '''Context manager to change backend temporarily in ipython sesson.
    It uses ipython magic to change temporarily from the ipython inline backend to
    an interactive backend of choice. It cannot be used outside ipython sessions nor
    to change backends different than inline -> interactive.
    Notes
    -----
    The first time ``interactive_backend`` context manager is called, any of the available
    interactive backends can be chosen. The following times, this same backend must be used
    unless the kernel is restarted.
    Parameters
    ----------
    backend : str, optional
        Interactive backend to use. It will be passed to ``%matplotlib`` magic, refer to
        its docs to see available options.
    Examples
    --------
    Inside an ipython session (i.e. a jupyter notebook) with the inline backend set:
    .. code::
        >>> import arviz as az
        >>> idata = az.load_arviz_data("centered_eight")
        >>> az.plot_posterior(idata) # inline
        >>> with az.interactive_backend():
        ...     az.plot_density(idata) # interactive
        >>> az.plot_trace(idata) # inline
    '''
    _first_use = True
    _backend = None

    def __init__(self, backend=''):
        self.backend = backend or matplotlib.rcParams["backend"].lower()

    def __enter__(self):
        '''Enter context manager.'''
        ipython = get_ipython()
        if ipython is None:
            raise RuntimeError(
                "`interactive_backend` context manager is intended for ipython sessions only")
        if not self._first_use and self._backend != self.backend:
            raise RuntimeError(
                f"Interactive backend has already been used with {self._backend} and can't be changed to {self.backend} without restarting the kernel")
        self._original_backend = matplotlib.get_backend().lower()
        if self._original_backend == "module://ipykernel.pylab.backend_inline":
            ipython.magic(f"%matplotlib {self.backend}")
            self._first_use = False
            self._backend = self.backend
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        '''Exit context manager.'''
        ipython = get_ipython()
        if ipython is not None and self._original_backend == "module://ipykernel.pylab.backend_inline":
            ipython.magic("%matplotlib inline")
        return False
