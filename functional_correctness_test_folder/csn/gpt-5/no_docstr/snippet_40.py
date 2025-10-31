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
    # Remember the chosen interactive backend across uses in the same kernel
    _chosen_backend = None

    def __init__(self, backend=''):
        self._requested_backend = (backend or '').strip()
        self._switched = False
        self._prev_backend = None

    def __enter__(self):
        ip = self._get_ipython_or_raise()
        import matplotlib

        self._prev_backend = matplotlib.get_backend()

        if not self._is_inline_backend(self._prev_backend):
            raise RuntimeError(
                "interactive_backend can only be used when the current backend is inline.")

        # Determine which backend to use this session
        if interactive_backend._chosen_backend is None:
            # First use in this kernel
            if self._requested_backend:
                candidate_list = [self._requested_backend]
            else:
                candidate_list = self._default_candidates()

            chosen = self._pick_first_working_backend(ip, candidate_list)
            if chosen is None:
                raise RuntimeError("No interactive matplotlib backend could be activated. "
                                   "Try specifying one explicitly, e.g., interactive_backend('qt'), "
                                   "and ensure the required GUI toolkit is installed.")
            interactive_backend._chosen_backend = chosen
        else:
            # Subsequent uses must match the originally chosen backend
            if self._requested_backend and self._requested_backend != interactive_backend._chosen_backend:
                raise RuntimeError(
                    f"interactive_backend already initialized with backend "
                    f"{interactive_backend._chosen_backend!r}; cannot switch to "
                    f"{self._requested_backend!r} without restarting the kernel."
                )
            # Activate the previously chosen backend
            self._activate_backend(ip, interactive_backend._chosen_backend)

        self._switched = True
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._switched:
            ip = self._get_ipython_or_raise()
            # Always return to inline
            try:
                ip.run_line_magic('matplotlib', 'inline')
            except Exception:
                pass
        # Do not suppress exceptions
        return False

    # Helper methods

    @staticmethod
    def _get_ipython_or_raise():
        try:
            from IPython import get_ipython
        except Exception as e:
            raise RuntimeError(
                "interactive_backend requires an IPython environment.") from e
        ip = get_ipython()
        if ip is None:
            raise RuntimeError(
                "interactive_backend requires an IPython environment.")
        return ip

    @staticmethod
    def _is_inline_backend(backend_name):
        # Typical inline backend identifiers
        if not backend_name:
            return False
        name = str(backend_name).lower()
        return 'inline' in name or 'matplotlib_inline' in name or name.startswith('module://matplotlib_inline')

    @staticmethod
    def _default_candidates():
        import sys
        # Start with common modern choices, then fallbacks
        candidates = [
            'qt5', 'qt', 'qt4',  # Qt family
            'tk',                # TkAgg
            'wx',                # wxAgg
            'gtk3', 'gtk',       # GTK
        ]
        # macOS specific candidate that uses Cocoa
        if sys.platform == 'darwin':
            candidates = ['osx'] + candidates
        return candidates

    def _activate_backend(self, ip, backend):
        ip.run_line_magic('matplotlib', backend)

    def _pick_first_working_backend(self, ip, candidates):
        import matplotlib

        for cand in candidates:
            try:
                self._activate_backend(ip, cand)
                # Verify backend changed away from inline
                current = matplotlib.get_backend()
                if not self._is_inline_backend(current):
                    return cand
            except Exception:
                # Restore inline after failed attempt to be safe
                try:
                    ip.run_line_magic('matplotlib', 'inline')
                except Exception:
                    pass
                continue
        return None
