
from dataclasses import dataclass, field
from typing import List, Dict, Tuple


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
    parameters: List[str] = field(default_factory=list)
    free_parameters: List[str] = field(default_factory=list)
    fixed_parameters: List[str] = field(default_factory=list)
    values_at_minimum: Dict[str, float] = field(default_factory=dict)
    errors_on_parameters: Dict[str, float] = field(default_factory=dict)
    covariance_matrix: Dict[Tuple[str, str],
                            float] = field(default_factory=dict)
    errors: Dict[str, float] = field(default_factory=dict)

    @property
    def correlation_matrix(self) -> dict[tuple[str, str], float]:
        return self._compute_correlation_matrix()

    def correlation_matrix(self) -> dict[tuple[str, str], float]:
        '''Calculate the correlation matrix (definition from iminuit) from the covariance matrix.'''
        return self._compute_correlation_matrix()

    def _compute_correlation_matrix(self) -> dict[tuple[str, str], float]:
        corr = {}
        # Only consider free parameters
        free = self.free_parameters
        for i, a in enumerate(free):
            for j, b in enumerate(free):
                key = (a, b)
                cov = self.covariance_matrix.get(
                    key, self.covariance_matrix.get((b, a), 0.0))
                var_a = self.covariance_matrix.get((a, a), 0.0)
                var_b = self.covariance_matrix.get((b, b), 0.0)
                if var_a == 0 or var_b == 0:
                    corr_val = 0.0
                else:
                    corr_val = cov / ((var_a ** 0.5) * (var_b ** 0.5))
                corr[key] = corr_val
        return corr
