
from dataclasses import dataclass, field
import numpy as np
from typing import Dict, Tuple


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
    values_at_minimum: Dict[str, float]
    errors_on_parameters: Dict[str, float]
    covariance_matrix: Dict[Tuple[str, str], float]
    errors: Dict[str, float] = field(default_factory=dict)
    _correlation_matrix: Dict[Tuple[str, str],
                              float] = field(default=None, init=False)

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
            self._correlation_matrix = self.calculate_correlation_matrix()
        return self._correlation_matrix

    def calculate_correlation_matrix(self) -> Dict[Tuple[str, str], float]:
        '''Calculate the correlation matrix (definition from iminuit) from the covariance matrix.'''
        covariance_matrix = np.array([[self.covariance_matrix.get(
            (param1, param2), 0) for param2 in self.free_parameters] for param1 in self.free_parameters])
        errors = np.array([self.errors_on_parameters[param]
                          for param in self.free_parameters])
        correlation_matrix = np.zeros_like(covariance_matrix)
        for i in range(len(self.free_parameters)):
            for j in range(len(self.free_parameters)):
                correlation_matrix[i, j] = covariance_matrix[i, j] / \
                    (errors[i] * errors[j]) if errors[i] * \
                    errors[j] != 0 else 0
        correlation_matrix_dict = {(self.free_parameters[i], self.free_parameters[j]): correlation_matrix[i, j] for i in range(
            len(self.free_parameters)) for j in range(len(self.free_parameters))}
        return correlation_matrix_dict
