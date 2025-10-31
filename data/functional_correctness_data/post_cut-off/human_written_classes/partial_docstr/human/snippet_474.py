from numpy.typing import NDArray
import numpy as np
from dataclasses import dataclass, field

@dataclass(frozen=True)
class DockQ:
    """
    Result of a *DockQ* calculation.

    If multiple poses were used to calculate *DockQ*, the attributes are arrays.

    Attributes
    ----------
    fnat : float or ndarray, dtype=float
        The fraction of reference contacts found in the pose relative to the total
        number of reference contacts.
    fnonnat : float or ndarray, dtype=float
        The fraction of non-reference contacts found in the pose relative to the total
        number of pose contacts.
    irmsd : float or ndarray, dtype=float
        The interface RMSD.
    lrmsd : float or ndarray, dtype=float
        The ligand RMSD.
    score : float or ndarray, dtype=float
        The DockQ score.
    n_poses : int or None
        The number of poses for which the *DockQ* was calculated.
        `None`, if the *DockQ* was calculated for an `AtomArray`.
    pose_receptor_index, pose_ligand_index, reference_receptor_index, reference_ligand_index : int or None
        The indices of the pose and reference chain that were included for *DockQ*
        computation.
        Only set, if called from `global_dockq()`.
    """
    fnat: float | NDArray[np.floating]
    fnonnat: float | NDArray[np.floating]
    irmsd: float | NDArray[np.floating]
    lrmsd: float | NDArray[np.floating]
    score: float | NDArray[np.floating] = field(init=False)
    n_poses: int | None = field(init=False)
    pose_receptor_index: int | None = None
    pose_ligand_index: int | None = None
    reference_receptor_index: int | None = None
    reference_ligand_index: int | None = None

    def __post_init__(self) -> None:
        score = np.nanmean([self.fnat, _scale(self.irmsd, 1.5), _scale(self.lrmsd, 8.5)], axis=0)
        n_poses = None if np.isscalar(score) else len(score)
        super().__setattr__('score', score)
        super().__setattr__('n_poses', n_poses)

    def for_pose(self, pose_index: int) -> 'DockQ':
        """
        Get the DockQ results for a specific pose index.

        Parameters
        ----------
        pose_index : int
            The index of the pose for which the DockQ results should be retrieved.

        Returns
        -------
        DockQ
            The DockQ results for the specified pose index.

        Raises
        ------
        IndexError
            If the `GlobalDockQ` object was computed for a single pose,
            i.e. `n_poses` is `None`.
        """
        if self.n_poses is None:
            raise IndexError('DockQ was computed for a single pose')
        return DockQ(self.fnat[pose_index].item(), self.fnonnat[pose_index].item(), self.irmsd[pose_index].item(), self.lrmsd[pose_index].item(), pose_receptor_index=self.pose_receptor_index, pose_ligand_index=self.pose_ligand_index, reference_receptor_index=self.reference_receptor_index, reference_ligand_index=self.reference_ligand_index)