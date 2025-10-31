
from dataclasses import dataclass
from typing import Dict, Tuple, List
import math


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
        if not hasattr(self, '_correlation_matrix'):
            self._correlation_matrix = self._calculate_correlation_matrix()
        return self._correlation_matrix

    def _calculate_correlation_matrix(self) -> Dict[Tuple[str, str], float]:
        '''Calculate the correlation matrix (definition from iminuit) from the covariance matrix.'''
        correlation_matrix = {}
        for (param_a, param_b), cov in self.covariance_matrix.items():
            if param_a in self.free_parameters and param_b in self.free_parameters:
                error_a = self.errors_on_parameters[param_a]
                error_b = self.errors_on_parameters[param_b]
                correlation = cov / (error_a * error_b)
                correlation_matrix[(param_a, param_b)] = correlation
        return correlation_matrix
