
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
        self._backend = backend
        self._shell = None
        self._old_backend = None

    def __enter__(self):
        '''Enter context manager.'''
        try:
            from IPython import get_ipython
        except ImportError:
            raise RuntimeError(
                "interactive_backend can only be used in an IPython session.")

        self._shell = get_ipython()
        if self._shell is None:
            raise RuntimeError(
                "interactive_backend can only be used in an IPython session.")

        # Get current backend
        import matplotlib
        self._old_backend = matplotlib.get_backend()

        # Only allow switching from inline to interactive
        if self._old_backend.lower() != "module://matplotlib_inline.backend_inline":
            raise RuntimeError(
                "interactive_backend can only be used when the current backend is 'inline'.")

        # Set or check the interactive backend
        if interactive_backend._chosen_backend is None:
            if not self._backend:
                # Default to 'qt' if available, else 'notebook', else 'tk'
                for candidate in ['qt', 'notebook', 'tk']:
                    try:
                        self._shell.run_line_magic('matplotlib', candidate)
                        interactive_backend._chosen_backend = candidate
                        break
                    except Exception:
                        continue
                if interactive_backend._chosen_backend is None:
                    raise RuntimeError(
                        "No suitable interactive backend found. Please specify one.")
            else:
                try:
                    self._shell.run_line_magic('matplotlib', self._backend)
                    interactive_backend._chosen_backend = self._backend
                except Exception as e:
                    raise RuntimeError(
                        f"Could not set backend '{self._backend}': {e}")
        else:
            if self._backend and self._backend != interactive_backend._chosen_backend:
                raise RuntimeError(
                    f"interactive_backend already set to '{interactive_backend._chosen_backend}'. "
                    f"Cannot switch to '{self._backend}' without restarting the kernel."
                )
            try:
                self._shell.run_line_magic(
                    'matplotlib', interactive_backend._chosen_backend)
            except Exception as e:
                raise RuntimeError(
                    f"Could not set backend '{interactive_backend._chosen_backend}': {e}")

        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        '''Exit context manager.'''
        if self._shell is not None:
            try:
                self._shell.run_line_magic('matplotlib', 'inline')
            except Exception:
                pass
        return False
