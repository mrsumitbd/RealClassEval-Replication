
from dataclasses import dataclass
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
    errors: Dict[str, float]

    @property
    def correlation_matrix(self) -> Dict[Tuple[str, str], float]:
        '''Calculate the correlation matrix (definition from iminuit) from the covariance matrix.'''
        corr_matrix = {}
        for (param_a, param_b), cov in self.covariance_matrix.items():
            error_a = self.errors_on_parameters.get(param_a, 0.0)
            error_b = self.errors_on_parameters.get(param_b, 0.0)
            if error_a == 0.0 or error_b == 0.0:
                corr = 0.0
            else:
                corr = cov / (error_a * error_b)
            corr_matrix[(param_a, param_b)] = corr
        return corr_matrix
