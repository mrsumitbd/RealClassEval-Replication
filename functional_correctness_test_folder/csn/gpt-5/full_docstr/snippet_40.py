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

    _chosen_backend = None

    def __init__(self, backend=''):
        '''Initialize context manager.'''
        self._requested_backend = backend
        self._ip = None
        self._active = False

    def __enter__(self):
        '''Enter context manager.'''
        try:
            from IPython import get_ipython
        except Exception as e:
            raise RuntimeError(
                "interactive_backend can only be used within an IPython session") from e

        ip = get_ipython()
        if ip is None:
            raise RuntimeError(
                "interactive_backend can only be used within an IPython session")

        try:
            import matplotlib as mpl
        except Exception as e:
            raise RuntimeError(
                "matplotlib is required to use interactive_backend") from e

        current_backend = str(mpl.get_backend()).lower()

        if "inline" not in current_backend:
            raise RuntimeError(
                "interactive_backend can only switch from the inline backend to an interactive backend"
            )

        # Determine the backend to use
        if interactive_backend._chosen_backend is None:
            if not self._requested_backend:
                raise ValueError(
                    "First use of interactive_backend requires specifying an interactive backend "
                    "(e.g., backend='qt', 'qt5', 'tk', 'osx', 'widget')."
                )
            interactive_backend._chosen_backend = str(self._requested_backend)
        else:
            if self._requested_backend and self._requested_backend != interactive_backend._chosen_backend:
                raise RuntimeError(
                    f"interactive_backend must reuse the initially chosen backend "
                    f"('{interactive_backend._chosen_backend}'); got '{self._requested_backend}'"
                )

        # Switch to the interactive backend via IPython magic
        try:
            ip.run_line_magic(
                'matplotlib', interactive_backend._chosen_backend)
        except Exception as e:
            raise RuntimeError(
                f"Failed to switch to interactive backend '{interactive_backend._chosen_backend}' via %matplotlib"
            ) from e

        self._ip = ip
        self._active = True
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        '''Exit context manager.'''
        if self._active and self._ip is not None:
            try:
                self._ip.run_line_magic('matplotlib', 'inline')
            except Exception:
                pass
        self._active = False
        self._ip = None
        return False
