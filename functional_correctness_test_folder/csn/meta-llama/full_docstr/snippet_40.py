
import IPython
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
        '''Initialize context manager.'''
        self.backend = backend

    def __enter__(self):
        '''Enter context manager.'''
        if not IPython.get_ipython():
            raise RuntimeError(
                "`interactive_backend` context manager is intended for use within ipython sessions")

        if interactive_backend._first_use:
            interactive_backend._backend = self.backend
            interactive_backend._first_use = False
        elif interactive_backend._backend != self.backend:
            raise ValueError(
                f"Backend has already been set to {interactive_backend._backend} and can't be changed to {self.backend} without restarting the kernel")

        self.ipython = get_ipython()
        self.original_backend = self.ipython.run_line_magic(
            'matplotlib', '--list').split()[0]
        if self.original_backend == 'inline':
            self.ipython.run_line_magic(
                'matplotlib', interactive_backend._backend)

    def __exit__(self, exc_type, exc_value, exc_tb):
        '''Exit context manager.'''
        if self.original_backend == 'inline':
            self.ipython.run_line_magic('matplotlib', 'inline')
