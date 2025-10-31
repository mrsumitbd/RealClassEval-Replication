
import hashlib
from typing import (
    Iterable,
    List,
    Tuple,
    Union,
    Dict,
    Set,
    Optional,
)

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

try:
    from tqdm import tqdm
except ImportError:  # pragma: no cover
    tqdm = lambda x, **kw: x


class DRFPUtil:
    @staticmethod
    def shingling_from_mol(
        in_mol: Chem.Mol,
        radius: int = 3,
        rings: bool = True,
        min_radius: int = 0,
        get_atom_indices: bool = False,
        root_central_atom: bool = True,
        include_hydrogens: bool = False,
    ) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        """
        Generate substructure shinglings for a single molecule.

        Parameters
        ----------
        in_mol : Chem.Mol
            RDKit molecule.
        radius : int
            Maximum radius for substructures.
        rings : bool
            Include full rings as substructures.
        min_radius : int
            Minimum radius (0 includes single atoms).
        get_atom_indices : bool
            Return mapping from shingle to atom indices.
        root_central_atom : bool
            Root the central atom in the SMILES.
        include_hydrogens : bool
            Include explicit hydrogens in the SMILES.

        Returns
        -------
        list or tuple
            List of shingle SMILES strings or a tuple of the list and a mapping.
        """
        shinglings: List[str] = []
        mapping: Dict[str, List[Set[int]]] = {}

        # Helper to generate substructure SMILES
        def _sub_smiles(atoms: Set[int]) -> str:
            sub = Chem.PathToSubmol(in_mol, list(atoms))
            return Chem.MolFragmentToSmiles(
                sub,
                atomsToUse=list(atoms),
                canonical=True,
                allBondsExplicit=False,
                allHsExplicit=include_hydrogens,
                rootedAtAtom=min(atoms) if root_central_atom else None,
            )

        # Generate substructures by radius
        for atom in in_mol.GetAtoms():
            idx = atom.GetIdx()
            for r in range(min_radius, radius + 1):
                atoms_in_radius = set(
                    Chem.rdmolops.GetMolFrags(
                        Chem.rdmolops.GetMolFragment(
                            in_mol, [idx], useBonds=True),
                        asMols=False,
                    )[0]
                )
                # Expand to radius r
                atoms = {idx}
                frontier = {idx}
                for _ in range(r):
                    new_frontier = set()
                    for f in frontier:
                        for nb in in_mol.GetAtomWithIdx(f).GetNeighbors():
                            if nb.GetIdx() not in atoms:
                                atoms.add(nb.GetIdx())
                                new_frontier.add(nb.GetIdx())
                    frontier = new_frontier
                smi = _sub_smiles(atoms)
                shinglings.append(smi)
                if get_atom_indices:
                    mapping.setdefault(smi, []).append(atoms)

        # Include full rings if requested
        if rings:
            ring_info = in_mol.GetRingInfo()
            for ring in ring_info.AtomRings():
                sm
