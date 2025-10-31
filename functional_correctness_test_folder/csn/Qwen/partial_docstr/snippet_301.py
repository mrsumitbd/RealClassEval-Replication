
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


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
        '''Calculate the correlation matrix (definition from iminuit) from the covariance matrix.'''
        correlation_matrix = {}
        for (param_a, param_b), cov_ab in self.covariance_matrix.items():
            err_a = self.errors_on_parameters[param_a]
            err_b = self.errors_on_parameters[param_b]
            if err_a != 0 and err_b != 0:
                correlation_matrix[(param_a, param_b)
                                   ] = cov_ab / (err_a * err_b)
        return correlation_matrix
