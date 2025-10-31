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
        self._requested_backend = backend.strip()
        self._enabled = False

    def __enter__(self):
        '''Enter context manager.'''
        try:
            from IPython import get_ipython
        except Exception as err:
            raise RuntimeError(
                "interactive_backend can only be used inside an IPython session") from err

        ip = get_ipython()
        if ip is None:
            raise RuntimeError(
                "interactive_backend can only be used inside an IPython session")

        try:
            import matplotlib
        except Exception as err:
            raise RuntimeError(
                "matplotlib is required to use interactive_backend") from err

        current_backend = str(matplotlib.get_backend()).lower()
        if "inline" not in current_backend:
            raise RuntimeError(
                "interactive_backend can only switch from the inline backend to an interactive backend"
            )

        # Determine which interactive backend to use for this and subsequent uses
        if interactive_backend._chosen_backend is None:
            chosen = self._requested_backend if self._requested_backend else "auto"
            interactive_backend._chosen_backend = chosen
        else:
            chosen = interactive_backend._chosen_backend
            if self._requested_backend and self._requested_backend != chosen:
                raise RuntimeError(
                    f"interactive_backend already initialized with backend '{chosen}'. "
                    f"Requested '{self._requested_backend}' does not match."
                )

        # Switch to interactive backend using IPython magic
        try:
            ip.run_line_magic(
                "matplotlib", interactive_backend._chosen_backend)
        except Exception as err:
            # If switching fails, reset chosen backend so future attempts can try again
            if interactive_backend._chosen_backend == self._requested_backend or (
                not self._requested_backend and interactive_backend._chosen_backend == "auto"
            ):
                interactive_backend._chosen_backend = None
            raise RuntimeError(
                f"Failed to switch to interactive backend '{interactive_backend._chosen_backend}' via %matplotlib"
            ) from err

        self._enabled = True
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        '''Exit context manager.'''
        if not self._enabled:
            return False
        try:
            from IPython import get_ipython
            ip = get_ipython()
            if ip is None:
                return False
            ip.run_line_magic("matplotlib", "inline")
        except Exception:
            # Do not suppress exceptions
            return False
        finally:
            self._enabled = False
        return False
