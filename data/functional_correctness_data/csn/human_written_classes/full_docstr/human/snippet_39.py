class Dask:
    """Class to toggle Dask states.

    Warnings
    --------
    Dask integration is an experimental feature still in progress. It can already be used
    but it doesn't work with all stats nor diagnostics yet.
    """
    dask_flag = False
    'bool: Enables Dask parallelization when set to True. Defaults to False.'
    dask_kwargs = None
    'dict: Additional keyword arguments for Dask configuration.\n    Defaults to an empty dictionary.'

    @classmethod
    def enable_dask(cls, dask_kwargs=None):
        """To enable Dask.

        Parameters
        ----------
        dask_kwargs : dict
            Dask related kwargs passed to :func:`~arviz.wrap_xarray_ufunc`.
        """
        cls.dask_flag = True
        cls.dask_kwargs = dask_kwargs

    @classmethod
    def disable_dask(cls):
        """To disable Dask."""
        cls.dask_flag = False
        cls.dask_kwargs = None