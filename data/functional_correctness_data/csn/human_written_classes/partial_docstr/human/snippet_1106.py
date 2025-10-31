import numpy as np
import time

class MetricObserver:
    """Metric observer.

    Wrapper of the metric to the observer object notify by the Observable
    class.

    Parameters
    ----------
    name : str
        The name of the metric
    metric : callable
        Metric function with this precise signature func(test, ref)
    mapping : dict
        Define the mapping between the iterate variable and the metric
        keyword: ``{'x_new':'name_var_1', 'y_new':'name_var_2'}``. To cancel
        the need of a variable, the dict value should be None:
        ``'y_new': None``.
    cst_kwargs : dict
        Keywords arguments of constant argument for the metric computation
    early_stopping : bool
        If True it will compute the convergence flag (default is ``False``)
    wind : int
        Window on with the convergence criteria is compute (default is ``6``)
    eps : float
        The level of criteria of convergence (default is ``1.0e-3``)

    """

    def __init__(self, name, metric, mapping, cst_kwargs, early_stopping=False, wind=6, eps=0.001):
        self.name = name
        self.metric = metric
        self.mapping = mapping
        self.cst_kwargs = cst_kwargs
        self.list_cv_values = []
        self.list_iters = []
        self.list_dates = []
        self.eps = eps
        self.wind = wind
        self.converge_flag = False
        self.early_stopping = early_stopping

    def __call__(self, signal):
        """Call Method.

        Wrapper the call from the observer signature to the metric
        signature.

        Parameters
        ----------
        signal : str
            A valid signal

        """
        kwargs = {}
        for key, key_value in self.mapping.items():
            if key_value is not None:
                kwargs[key_value] = getattr(signal, key)
        kwargs.update(self.cst_kwargs)
        self.list_iters.append(signal.idx)
        self.list_dates.append(time.time())
        self.list_cv_values.append(self.metric(**kwargs))
        if self.early_stopping:
            self.is_converge()

    def is_converge(self):
        """Check convergence.

        Return ``True`` if the convergence criteria is matched.

        """
        if len(self.list_cv_values) < self.wind:
            return
        start_idx = -self.wind
        mid_idx = -(self.wind // 2)
        old_mean = np.array(self.list_cv_values[start_idx:mid_idx]).mean()
        current_mean = np.array(self.list_cv_values[mid_idx:]).mean()
        normalize_residual_metrics = np.abs(old_mean - current_mean) / np.abs(old_mean)
        self.converge_flag = normalize_residual_metrics < self.eps

    def retrieve_metrics(self):
        """Retrieve metrics.

        Return the convergence metrics saved with the corresponding
        iterations.

        Returns
        -------
        dict
            Convergence metrics

        """
        time_val = np.array(self.list_dates)
        if time_val.size >= 1:
            time_val -= time_val[0]
        return {'time': time_val, 'index': self.list_iters, 'values': self.list_cv_values}