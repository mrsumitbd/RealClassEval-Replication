import numpy as np

class CoxPHOptimizer:
    """Helper class for fitting the Cox proportional hazards model.

    This class computes the negative log-likelihood, its gradient, and the
    Hessian matrix for the Cox model. It is used internally by
    :class:`CoxPHSurvivalAnalysis`.

    Parameters
    ----------
    X : ndarray, shape=(n_samples, n_features)
        The feature matrix.

    event : ndarray, shape=(n_samples,)
        The event indicator.

    time : ndarray, shape=(n_samples,)
        The event/censoring times.

    alpha : ndarray, shape=(n_features,)
        The regularization parameters.

    ties : {'breslow', 'efron'}
        The method to handle tied event times.
    """

    def __init__(self, X, event, time, alpha, ties):
        o = np.argsort(-time, kind='mergesort')
        self.x = X[o, :]
        self.event = event[o]
        self.time = time[o]
        self.alpha = alpha
        self.no_alpha = np.all(self.alpha < np.finfo(self.alpha.dtype).eps)
        self._is_breslow = ties == 'breslow'

    def nlog_likelihood(self, w):
        """Compute negative partial log-likelihood

        Parameters
        ----------
        w : array, shape = (n_features,)
            Estimate of coefficients

        Returns
        -------
        loss : float
            Average negative partial log-likelihood
        """
        time = self.time
        n_samples = self.x.shape[0]
        breslow = self._is_breslow
        xw = np.dot(self.x, w)
        loss = 0
        risk_set = 0
        k = 0
        while k < n_samples:
            ti = time[k]
            numerator = 0
            n_events = 0
            risk_set2 = 0
            while k < n_samples and ti == time[k]:
                if self.event[k]:
                    numerator += xw[k]
                    risk_set2 += np.exp(xw[k])
                    n_events += 1
                else:
                    risk_set += np.exp(xw[k])
                k += 1
            if n_events > 0:
                if breslow:
                    risk_set += risk_set2
                    loss -= (numerator - n_events * np.log(risk_set)) / n_samples
                else:
                    numerator /= n_events
                    for _ in range(n_events):
                        risk_set += risk_set2 / n_events
                        loss -= (numerator - np.log(risk_set)) / n_samples
        return loss + np.sum(self.alpha * np.square(w)) / (2.0 * n_samples)

    def update(self, w, offset=0):
        """Compute gradient and Hessian matrix with respect to `w`."""
        time = self.time
        x = self.x
        breslow = self._is_breslow
        exp_xw = np.exp(offset + np.dot(x, w))
        n_samples, n_features = x.shape
        gradient = np.zeros((1, n_features), dtype=w.dtype)
        hessian = np.zeros((n_features, n_features), dtype=w.dtype)
        inv_n_samples = 1.0 / n_samples
        risk_set = 0
        risk_set_x = np.zeros((1, n_features), dtype=w.dtype)
        risk_set_xx = np.zeros((n_features, n_features), dtype=w.dtype)
        k = 0
        while k < n_samples:
            ti = time[k]
            n_events = 0
            numerator = 0
            risk_set2 = 0
            risk_set_x2 = np.zeros_like(risk_set_x)
            risk_set_xx2 = np.zeros_like(risk_set_xx)
            while k < n_samples and ti == time[k]:
                xk = x[k:k + 1]
                xx = np.dot(xk.T, xk)
                if self.event[k]:
                    numerator += xk
                    risk_set2 += exp_xw[k]
                    risk_set_x2 += exp_xw[k] * xk
                    risk_set_xx2 += exp_xw[k] * xx
                    n_events += 1
                else:
                    risk_set += exp_xw[k]
                    risk_set_x += exp_xw[k] * xk
                    risk_set_xx += exp_xw[k] * xx
                k += 1
            if n_events > 0:
                if breslow:
                    risk_set += risk_set2
                    risk_set_x += risk_set_x2
                    risk_set_xx += risk_set_xx2
                    z = risk_set_x / risk_set
                    gradient -= (numerator - n_events * z) * inv_n_samples
                    a = risk_set_xx / risk_set
                    b = np.dot(z.T, z)
                    hessian += n_events * (a - b) * inv_n_samples
                else:
                    numerator /= n_events
                    for _ in range(n_events):
                        risk_set += risk_set2 / n_events
                        risk_set_x += risk_set_x2 / n_events
                        risk_set_xx += risk_set_xx2 / n_events
                        z = risk_set_x / risk_set
                        gradient -= (numerator - z) * inv_n_samples
                        a = risk_set_xx / risk_set
                        b = np.dot(z.T, z)
                        hessian += (a - b) * inv_n_samples
        if not self.no_alpha:
            gradient += self.alpha * inv_n_samples * w
            diag_idx = np.diag_indices(n_features)
            hessian[diag_idx] += self.alpha * inv_n_samples
        self.gradient = gradient.ravel()
        self.hessian = hessian