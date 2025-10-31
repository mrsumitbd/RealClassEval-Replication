import numpy as np
import numpy.typing as npt
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypeVar, cast

@dataclass
class BaseFitResult:
    """Base fit result.

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
    """
    parameters: list[str]
    free_parameters: list[str]
    fixed_parameters: list[str]
    values_at_minimum: dict[str, float]
    errors_on_parameters: dict[str, float]
    covariance_matrix: dict[tuple[str, str], float]
    errors: npt.NDArray[Any]

    @property
    def correlation_matrix(self) -> dict[tuple[str, str], float]:
        """The correlation matrix of the free parameters.

        These values are derived from the covariance matrix values stored in the fit.

        Note:
            This property caches the correlation matrix value so we don't have to calculate it every time.

        Args:
            None
        Returns:
            The correlation matrix of the fit result.
        """
        try:
            return self._correlation_matrix
        except AttributeError:

            def corr(i_name: str, j_name: str) -> float:
                """Calculate the correlation matrix (definition from iminuit) from the covariance matrix."""
                value = self.covariance_matrix[i_name, j_name] / (np.sqrt(self.covariance_matrix[i_name, i_name] * self.covariance_matrix[j_name, j_name]) + 1e-100)
                return float(value)
            matrix: dict[tuple[str, str], float] = {}
            for i_name in self.free_parameters:
                for j_name in self.free_parameters:
                    matrix[i_name, j_name] = corr(i_name, j_name)
            self._correlation_matrix = matrix
        return self._correlation_matrix