
import matplotlib.pyplot as plt


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

    def __init__(self, backend=''):
        self.backend = backend
        self.original_backend = plt.get_backend()

    def __enter__(self):
        '''Enter context manager.'''
        if self.backend:
            plt.switch_backend(self.backend)

    def __exit__(self, exc_type, exc_value, exc_tb):
        '''Exit context manager.'''
        plt.switch_backend(self.original_backend)
