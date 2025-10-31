class UpdatableMixin:
    """Transformers that may update their params, like ARIMAs"""

    def _check_endog(self, y):
        if y is None:
            raise ValueError('endog array cannot be None when updating')

    def update_and_transform(self, y, X=None, **kwargs):
        """Update the params and return the transformed arrays

        Parameters
        ----------
        y : array-like or None, shape=(n_samples,)
            The endogenous (time-series) array.

        X : array-like or None, shape=(n_samples, n_features)
            The exogenous array of additional covariates.

        **kwargs : keyword args
            Keyword arguments required by the transform function.
        """