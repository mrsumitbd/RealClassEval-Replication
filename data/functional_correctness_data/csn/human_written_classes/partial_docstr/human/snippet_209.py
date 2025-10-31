import matplotlib as mpl

class set_interactive_backend:
    """
    Manually set the `matplotlib` backend used for generating
    interactive plots.

    Whereas `hypertools.plot`'s `mpl_backend` keyword argument can be
    used to specify the backend for a single plot,
    `hypertools.set_interactive_backend` is useful for doing so for
    multiple (or all) interactive plots at once, and can be in two
    different ways:

    1. directly, to change the backend for all subsequent interactive
       plots
          ```
          import hypertools as hyp
          geo = hyp.load('weights_avg')

          geo.plot(interactive=True)          # uses the default backend

          hyp.set_interactive_backend('TkAgg')
          geo.plot(interactive=True)          # uses the TkInter backend
          geo.plot(animate=True)              # uses the TkInter backend
          ```

    2. as a context manager with the `with` statement, to temporarily
       change the backend
          ```
          import hypertools as hyp
          geo = hyp.load('weights_avg')

          geo.plot(interactive=True)          # uses the default backend

          with hyp.set_interactive_backend('TkAgg'):
              geo.plot(interactive=True)      # uses the TkInter backend

          geo.plot(animate=True)              # uses the default backend
          ```

    Parameters
    ----------
    backend : str
        The `matplotlib` backend to use for interactive plots, either
        temporarily (when used as a context manager with `with`) or for
        the life of the interpreter (when called as a function)

    Notes
    -----
    1. `set_interactive_backend` is technically a class, but it
       shouldn't typically be used as one and is only designed this way
       to enable it to work as both a regular function and a context
       manager.
    2. Calling this directly does *not* immediately change the plotting
       backend; it changes the backend `hypertools` will use to create
       interactive plots going forward.
    3. However, when used as a context manager, the backend passed to
       `hypertools.set_interactive_backend` will be used for *all* plots
       created inside the context block, regardless of whether:
         - they are interactive/animated or static
         - the `mpl_backend` keyword argument is passed to
           `hypertools.plot`
         - they were created with `hypertools`, `matplotlib`, or a
           different `matplotlib`-based library (e.g., `seaborn`,
           `quail`, `umap-learn`)
       There are a few reasons for this behavior:
         - being able to skip inspecting the arguments passed to each
           `hypertools.plot` call means almost no overhead is added for
           calls after the first, and makes wrapping multiple calls much
           more efficient
         - the plotting backend is an attribute of `matplotlib` itself
           and `matplotlib` doesn't support running multiple backends
           simultaneously in the same namespace, so it's impossible to
           avoid it affecting other `matplotlib`-based plotting libraries
         - it's reasonable to assume this was the desired outcome when
           multiple plots are generated inside a context block, since A)
           the context block will always have been created manually by
           the user, and B) the API provides multiple other ways to set
           the backend without this effect
    3. The `manage_backend` decorator for `hypertools.plot` determines
       whether it's being called inside the
       `hypertools.set_interactive_backend` context manager by checking
       the value of a global variable (`IN_SET_CONTEXT`), which is
       switched to `True` when the the runtime context is entered and
       `False` when it's exited. This definitely isn't an ideal setup
       and could probably be refactored out in the v2.0 overhaul, but
       for now the alternatives are A) using something like
       `inspect.getframeinfo` or `traceback.extract_stack` to look for
       the context manager every time `hypertools.plot` is called, or B)
       re-running the same runtime argument checks every time, either of
       which would be much less efficient. So for now, the current setup
       is probably good enough.
    """

    def __init__(self, backend):
        global BACKEND_WARNING, HYPERTOOLS_BACKEND
        self.old_interactive_backend = HYPERTOOLS_BACKEND.normalize()
        self.old_backend_warning = BACKEND_WARNING
        self.new_interactive_backend = HypertoolsBackend(backend).normalize()
        self.new_is_different = self.new_interactive_backend != self.old_interactive_backend
        self.backend_switched = False
        if self.new_is_different:
            HYPERTOOLS_BACKEND = self.new_interactive_backend
            BACKEND_WARNING = None

    def __enter__(self):
        global IN_SET_CONTEXT
        IN_SET_CONTEXT = True
        self.curr_backend = HypertoolsBackend(mpl.get_backend()).normalize()
        if self.curr_backend != self.new_interactive_backend:
            self.backend_switched = True
            switch_backend(self.new_interactive_backend)

    def __exit__(self, exc_type, exc_value, traceback):
        global BACKEND_WARNING, HYPERTOOLS_BACKEND, IN_SET_CONTEXT
        IN_SET_CONTEXT = False
        if self.new_is_different:
            HYPERTOOLS_BACKEND = self.old_interactive_backend
            BACKEND_WARNING = self.old_backend_warning
        if self.backend_switched:
            reset_backend(self.curr_backend)