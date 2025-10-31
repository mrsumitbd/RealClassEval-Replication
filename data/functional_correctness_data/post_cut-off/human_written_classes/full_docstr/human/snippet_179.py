import torch
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Self, cast

@dataclass(kw_only=True)
class DeformGradMixin:
    """Mixin for states that support deformation gradients."""
    reference_cell: torch.Tensor
    _system_attributes: ClassVar[set[str]] = {'reference_cell'}
    if TYPE_CHECKING:
        row_vector_cell: torch.Tensor

    @property
    def reference_row_vector_cell(self) -> torch.Tensor:
        """Get the original unit cell in terms of row vectors."""
        return self.reference_cell.mT

    @reference_row_vector_cell.setter
    def reference_row_vector_cell(self, value: torch.Tensor) -> None:
        """Set the original unit cell in terms of row vectors."""
        self.reference_cell = value.mT

    @staticmethod
    def _deform_grad(reference_row_vector_cell: torch.Tensor, row_vector_cell: torch.Tensor) -> torch.Tensor:
        """Calculate the deformation gradient from original cell to current cell.

        Returns:
            The deformation gradient
        """
        return torch.linalg.solve(reference_row_vector_cell, row_vector_cell).transpose(-2, -1)

    def deform_grad(self) -> torch.Tensor:
        """Calculate the deformation gradient from original cell to current cell.

        Returns:
            The deformation gradient
        """
        return self._deform_grad(self.reference_row_vector_cell, self.row_vector_cell)