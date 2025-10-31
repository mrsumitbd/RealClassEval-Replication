from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt
from typing import Dict, Tuple, List


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
        cov = self.covariance_matrix
        result: Dict[Tuple[str, str], float] = {}

        # Determine the parameter order to include in the correlation matrix
        params = list(self.free_parameters)
        if not params:
            # Fall back to parameters detected from covariance matrix keys
            detected = set()
            for a, b in cov.keys():
                detected.add(a)
                detected.add(b)
            params = sorted(detected)

        # Gather variances
        variances: Dict[str, float] = {}
        for p in params:
            variances[p] = cov.get((p, p), 0.0)

        # Build full symmetric correlation matrix over free parameters
        for i, a in enumerate(params):
            va = variances.get(a, 0.0)
            for b in params[i:]:
                vb = variances.get(b, 0.0)
                cij = cov.get((a, b))
                if cij is None:
                    cij = cov.get((b, a), 0.0)

                denom = sqrt(va * vb) if va > 0.0 and vb > 0.0 else 0.0
                if denom > 0.0:
                    corr = cij / denom
                else:
                    # If variance is zero or missing, correlation is undefined; set to 0.0
                    # Diagonal becomes 0.0 in this case; otherwise off-diagonals 0.0 as well.
                    corr = 0.0

                result[(a, b)] = corr
                result[(b, a)] = corr

        return result
