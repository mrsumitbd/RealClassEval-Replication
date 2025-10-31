
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
        Interactive backend to use. It will be pass
    ed to ``%matplotlib`` magic, refer to
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
    # Class variable to remember the chosen interactive backend across context managers
    _stored_backend = None

    def __init__(self, backend=''):
        self.backend = backend
        self._original_backend = None

    def __enter__(self):
        ip = get_ipython()
        if ip is None:
            raise RuntimeError(
                "interactive_backend can only be used inside an IPython session")

        # Determine the interactive backend to use
        if interactive_backend._stored_backend is None:
            # First time: store the chosen backend (or default to 'qt')
            if not self.backend:
                # Try to pick a sensible default interactive backend
                # Prefer 'qt' if available, otherwise fall back to 'tk'
                try:
                    import PyQt5  # noqa: F401
                    self.backend = 'qt'
                except Exception:
                    self.backend = 'tk'
            interactive_backend._stored_backend = self.backend
        else:
            # Subsequent times: enforce the same backend
            if self.backend and self.backend != interactive_backend._stored_backend:
                raise RuntimeError(
                    f"interactive_backend was first used with backend '{interactive_backend._stored_backend}'. "
                    f"Cannot change to '{self.backend}'."
                )
            self.backend = interactive_backend._stored_backend

        # Save the current backend
        self._original_backend = matplotlib.get_backend()

        # Ensure we are switching from inline to an interactive backend
        if self._original_backend.lower() != 'inline':
            raise RuntimeError(
                f"interactive_backend can only switch from 'inline' backend, "
                f"but current backend is '{self._original_backend}'."
            )

        # Switch to the interactive backend
        ip.run_line_magic('matplotlib', self.backend)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        ip = get_ipython()
        if ip is None:
            return False  # propagate exception if any

        # Restore the original backend
        if self._original_backend:
            ip.run_line_magic('matplotlib', self._original_backend)
        return False  # do not suppress exceptions
