from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt
from typing import Dict, List, Optional, Tuple


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

    _correlation_matrix_cache: Optional[Dict[Tuple[str, str], float]] = field(
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
        if self._correlation_matrix_cache is None:
            self._correlation_matrix_cache = self.calculate_correlation_matrix()
        return self._correlation_matrix_cache

    def calculate_correlation_matrix(self) -> dict[tuple[str, str], float]:
        '''Calculate the correlation matrix (definition from iminuit) from the covariance matrix.'''
        corr: Dict[Tuple[str, str], float] = {}

        def cov(a: str, b: str) -> Optional[float]:
            if (a, b) in self.covariance_matrix:
                return self.covariance_matrix[(a, b)]
            if (b, a) in self.covariance_matrix:
                return self.covariance_matrix[(b, a)]
            return None

        # Precompute standard deviations for free parameters
        std: Dict[str, Optional[float]] = {}
        for p in self.free_parameters:
            v = cov(p, p)
            if v is None or v <= 0.0:
                std[p] = None
            else:
                std[p] = sqrt(v)

        # Build full symmetric correlation matrix for free parameters
        for a in self.free_parameters:
            for b in self.free_parameters:
                if a == b:
                    # Diagonal correlation is 1 if variance is defined, else 1 (conventional fallback)
                    corr[(a, b)] = 1.0
                    continue

                va = std.get(a)
                vb = std.get(b)
                cab = cov(a, b)

                if va is None or vb is None or cab is None:
                    # If missing information, default to 0.0 correlation off-diagonal
                    corr[(a, b)] = 0.0
                else:
                    denom = va * vb
                    corr[(a, b)] = cab / denom if denom != 0.0 else 0.0

        return corr
