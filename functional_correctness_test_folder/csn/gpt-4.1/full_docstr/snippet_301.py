
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Any


@dataclass
class BaseFitResult:
    '''Base fit result.
    This represents the most basic fit result.
    Attributes:
        parameters: Names of the parameters used in the fit.
        free_parameters: Names of the free parameters used in the fit.
        fixed_parameters: Names of the fixed parameters used in the fit.
        values_at_minimum: Contains the values of the full RP fit function at the minimum. Keys are the
            names of parameters, while values are the numerical values at convergence.
        errors_on_parameters: Contains the values of the errors associated with the parameters
            determined via the fit.
        covariance_matrix: Contains the values of the covariance matrix. Keys are tuples
            with (param_name_a, param_name_b), and the values are covariance between the specified parameters.
            Note that fixed parameters are _not_ included in this matrix.
        errors: Store the errors associated with the component fit function.
    '''
    parameters: List[str]
    free_parameters: List[str]
    fixed_parameters: List[str]
    values_at_minimum: Dict[str, float]
    errors_on_parameters: Dict[str, float]
    covariance_matrix: Dict[Tuple[str, str], float]
    errors: Any = None

    _correlation_matrix_cache: Dict[Tuple[str, str], float] = field(
        default=None, init=False, repr=False)

    @property
    def correlation_matrix(self) -> dict[tuple[str, str], float]:
        '''The correlation matrix of the free parameters.
        These values are derived from the covariance matrix values stored in the fit.
        Note:
            This property caches the correlation matrix value so we don't have to calculate it every time.
        Args:
            None
        Returns:
            The correlation matrix of the fit result.
        '''
        if self._correlation_matrix_cache is not None:
            return self._correlation_matrix_cache
        self._correlation_matrix_cache = self._compute_correlation_matrix()
        return self._correlation_matrix_cache

    def _compute_correlation_matrix(self) -> dict[tuple[str, str], float]:
        '''Calculate the correlation matrix (definition from iminuit) from the covariance matrix.'''
        corr = {}
        free = self.free_parameters
        for i, a in enumerate(free):
            for j, b in enumerate(free):
                key = (a, b)
                cov = self.covariance_matrix.get(
                    key, self.covariance_matrix.get((b, a), 0.0))
                var_a = self.covariance_matrix.get((a, a), 0.0)
                var_b = self.covariance_matrix.get((b, b), 0.0)
                if var_a == 0 or var_b == 0:
                    corr[key] = 0.0
                else:
                    corr[key] = cov / (var_a ** 0.5 * var_b ** 0.5)
        return corr

    def correlation_matrix(self) -> dict[tuple[str, str], float]:
        '''Calculate the correlation matrix (definition from iminuit) from the covariance matrix.'''
        return self._compute_correlation_matrix()
