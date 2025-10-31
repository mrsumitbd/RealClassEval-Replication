
from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt
from typing import Dict, Tuple, List, Optional


@dataclass
class BaseFitResult:
    """Base fit result.
    This represents the most basic fit result.
    Attributes:
        parameters: Names of the parameters used in the fit.
        free_parameters: Names of the free parameters used in the fit.
        fixed_parameters: Names of the fixed parameters used in the fit.
        values_at_minimum: Contains the values of the full RP fit function at the minimum.
            Keys are the names of parameters, while values are the numerical values at convergence.
        errors_on_parameters: Contains the values of the errors associated with the parameters
            determined via the fit.
        covariance_matrix: Contains the values of the covariance matrix. Keys are tuples
            with (param_name_a, param_name_b), and the values are covariance between the specified parameters.
            Note that fixed parameters are _not_ included in this matrix.
        errors: Store the errors associated with the component fit function.
    """
    parameters: List[str] = field(default_factory=list)
    free_parameters: List[str] = field(default_factory=list)
    fixed_parameters: List[str] = field(default_factory=list)
    values_at_minimum: Dict[str, float] = field(default_factory=dict)
    errors_on_parameters: Dict[str, float] = field(default_factory=dict)
    covariance_matrix: Dict[Tuple[str, str],
                            float] = field(default_factory=dict)
    errors: Dict[str, float] = field(default_factory=dict)

    # internal cache for the correlation matrix
    _correlation_matrix: Optional[Dict[Tuple[str, str], float]] = field(
        default=None, init=False, repr=False)

    @property
    def correlation_matrix(self) -> Dict[Tuple[str, str], float]:
        """The correlation matrix of the free parameters.
        These values are derived from the covariance matrix values stored in the fit.
        Note:
            This property caches the correlation matrix value so we don't have to calculate it every time.
        Args:
            None
        Returns:
            The correlation matrix of the fit result.
        """
        if self._correlation_matrix is None:
            self._correlation_matrix = self._calculate_correlation_matrix()
        return self._correlation_matrix

    def _calculate_correlation_matrix(self) -> Dict[Tuple[str, str], float]:
        """Calculate the correlation matrix (definition from iminuit) from the covariance matrix."""
        corr: Dict[Tuple[str, str], float] = {}
        for a in self.free_parameters:
            var_a = self.covariance_matrix.get((a, a), 0.0)
            for b in self.free_parameters:
                if a == b:
                    corr[(a, b)] = 1.0
                else:
                    cov_ab = self.covariance_matrix.get(
                        (a, b), self.covariance_matrix.get((b, a), 0.0))
                    var_b = self.covariance_matrix.get((b, b), 0.0)
                    denom = sqrt(
                        var_a * var_b) if var_a > 0 and var_b > 0 else 0.0
                    corr[(a, b)] = cov_ab / denom if denom != 0 else 0.0
        return corr
