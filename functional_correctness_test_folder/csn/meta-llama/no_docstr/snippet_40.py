
import matplotlib
from IPython import get_ipython


class interactive_backend:
    '''Context manager to change backend temporarily in ipython session.
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
    _stored_backend = None

    def __init__(self, backend=''):
        self.backend = backend

    def __enter__(self):
        ipython = get_ipython()
        if ipython is None:
            raise RuntimeError(
                "`interactive_backend` context manager is intended for use within ipython sessions")
        if not matplotlib.is_interactive() or matplotlib.get_backend() == "module://ipykernel.pylab.backend_inline":
            if interactive_backend._first_use:
                if self.backend:
                    ipython.run_line_magic('matplotlib', self.backend)
                else:
                    ipython.run_line_magic('matplotlib', '')
                interactive_backend._stored_backend = matplotlib.get_backend()
                interactive_backend._first_use = False
            else:
                if matplotlib.get_backend() != interactive_backend._stored_backend:
                    raise RuntimeError(f"Backend has already been set to {interactive_backend._stored_backend} "
                                       "and it can't be changed to a different one")
                ipython.run_line_magic(
                    'matplotlib', self.backend if self.backend else 'qt5')
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        ipython = get_ipython()
        ipython.run_line_magic('matplotlib', 'inline')
