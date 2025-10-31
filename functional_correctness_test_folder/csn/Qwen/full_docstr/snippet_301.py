
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import numpy as np


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
    errors: Dict[str, float]
    _correlation_matrix: Dict[Tuple[str, str],
                              float] = field(init=False, default=None)

    @property
    def correlation_matrix(self) -> Dict[Tuple[str, str], float]:
        '''The correlation matrix of the free parameters.
        These values are derived from the covariance matrix values stored in the fit.
        Note:
            This property caches the correlation matrix value so we don't have to calculate it every time.
        Args:
            None
        Returns:
            The correlation matrix of the fit result.
        '''
        if self._correlation_matrix is None:
            self._correlation_matrix = self._calculate_correlation_matrix()
        return self._correlation_matrix

    def _calculate_correlation_matrix(self) -> Dict[Tuple[str, str], float]:
        '''Calculate the correlation matrix (definition from iminuit) from the covariance matrix.'''
        free_params = self.free_parameters
        cov_matrix = np.array([[self.covariance_matrix.get(
            (p1, p2), 0.0) for p2 in free_params] for p1 in free_params])
        errors = np.array([self.errors_on_parameters[p] for p in free_params])
        corr_matrix = cov_matrix / np.outer(errors, errors)
        return {(free_params[i], free_params[j]): corr_matrix[i, j] for i in range(len(free_params)) for j in range(len(free_params))}
