
from dataclasses import dataclass
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
    parameters: list[str]
    free_parameters: list[str]
    fixed_parameters: list[str]
    values_at_minimum: dict[str, float]
    errors_on_parameters: dict[str, float]
    covariance_matrix: dict[tuple[str, str], float]
    errors: dict[str, float]

    @property
    def correlation_matrix(self) -> dict[tuple[str, str], float]:
        return self._calculate_correlation_matrix()

    def _calculate_correlation_matrix(self) -> dict[tuple[str, str], float]:
        '''Calculate the correlation matrix (definition from iminuit) from the covariance matrix.'''
        correlation_matrix = {}
        for (param_a, param_b), cov in self.covariance_matrix.items():
            error_a = self.errors_on_parameters[param_a]
            error_b = self.errors_on_parameters[param_b]
            correlation = cov / (error_a * error_b)
            correlation_matrix[(param_a, param_b)] = correlation
        return correlation_matrix
