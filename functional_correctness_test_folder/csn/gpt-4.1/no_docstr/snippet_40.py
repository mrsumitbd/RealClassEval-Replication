
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
    _used_backend = None

    def __init__(self, backend=''):
        self.backend = backend
        self._ipython = None
        self._old_backend = None

    def __enter__(self):
        try:
            from IPython import get_ipython
        except ImportError:
            raise RuntimeError(
                "interactive_backend can only be used in IPython sessions.")
        self._ipython = get_ipython()
        if self._ipython is None:
            raise RuntimeError(
                "interactive_backend can only be used in IPython sessions.")

        # Get current backend
        self._old_backend = self._ipython.run_line_magic('matplotlib', '')
        # The above returns None, so we need another way to get the current backend
        # Use matplotlib.get_backend()
        import matplotlib
        self._old_backend = matplotlib.get_backend()

        # Only allow switching from inline to interactive
        if self._old_backend.lower().startswith('inline'):
            # Only allow first backend to be set, then must be the same
            if interactive_backend._used_backend is None:
                if self.backend:
                    backend_to_use = self.backend
                else:
                    backend_to_use = 'auto'
                self._ipython.run_line_magic('matplotlib', backend_to_use)
                # Get the backend actually set
                import matplotlib
                interactive_backend._used_backend = matplotlib.get_backend()
            else:
                # Check if requested backend matches the one already used
                if self.backend and self.backend.lower() != interactive_backend._used_backend.lower():
                    raise RuntimeError(
                        f"interactive_backend already set to {interactive_backend._used_backend}, "
                        f"cannot switch to {self.backend} without restarting the kernel."
                    )
                # Set to the already used backend
                self._ipython.run_line_magic(
                    'matplotlib', interactive_backend._used_backend)
        else:
            raise RuntimeError(
                "interactive_backend can only be used when the current backend is 'inline'.")

        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Restore the inline backend
        if self._ipython is not None:
            self._ipython.run_line_magic('matplotlib', 'inline')
