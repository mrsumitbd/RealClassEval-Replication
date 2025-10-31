
from typing import List, Tuple, Dict, Set, Union, Iterable
import numpy as np

from rdkit import Chem
from rdkit.Chem import Mol
from rdkit.Chem.rdmolops import GetShortestPath


class DRFPUtil:

    @staticmethod
    def shingling_from_mol(
        in_mol: Mol,
        radius: int = 3,
        rings: bool = True,
        min_radius: int = 0,
        get_atom_indices: bool = False,
        root_central_atom: bool = True,
        include_hydrogens: bool = False
    ) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        from collections import defaultdict

        mol = Chem.RWMol(in_mol)
        if not include_hydrogens:
            mol = Chem.RemoveHs(mol)
        n_atoms = mol.GetNumAtoms()
        shinglings = []
        atom_indices_map = defaultdict(list)

        # Rings
        if rings:
            ssr = Chem.GetSymmSSSR(mol)
            for ring in ssr:
                ring_atoms = list(ring)
                submol = Chem.PathToSubmol(mol, ring_atoms)
                smiles = Chem.MolToSmiles(
                    submol, rootedAtAtom=ring_atoms[0] if root_central_atom else -1, canonical=True)
                shinglings.append(smiles)
                if get_atom_indices:
                    atom_indices_map[smiles].append(set(ring_atoms))

        # Spheres
        for atom_idx in range(n_atoms):
            for rad in range(min_radius, radius+1):
                env = Chem.FindAtomEnvironmentOfRadiusN(mol, rad, atom_idx)
                if not env:
                    continue
                atoms_in_env = set()
                for bidx in env:
                    bond = mol.GetBondWithIdx(bidx)
                    atoms_in_env.add(bond.GetBeginAtomIdx())
                    atoms_in_env.add(bond.GetEndAtomIdx())
                atoms_in_env.add(atom_idx)
                submol = Chem.PathToSubmol(mol, env)
                try:
                    smiles = Chem.MolToSmiles(
                        submol,
                        rootedAtAtom=atom_idx if root_central_atom else -1,
                        canonical=True
                    )
                except Exception:
                    continue
                shinglings.append(smiles)
                if get_atom_indices:
                    atom_indices_map[smiles].append(set(atoms_in_env))

        if get_atom_indices:
            return shinglings, dict(atom_indices_map)
        else:
            return shinglings

    @staticmethod
    def internal_encode(
        in_smiles: str,
        radius: int = 3,
        min_radius: int = 0,
        rings: bool = True,
        get_atom_indices: bool = False,
        root_central_atom: bool = True,
        include_hydrogens: bool = False
    ) -> Union[
        Tuple[np.ndarray, np.ndarray],
        Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]
    ]:
        mol = Chem.MolFromSmiles(in_smiles)
        if mol is None:
            raise ValueError(f"Invalid SMILES: {in_smiles}")
        if get_atom_indices:
            shinglings, atom_indices_map = DRFPUtil.shingling_from_mol(
                mol, radius=radius, rings=rings, min_radius=min_radius,
                get_atom_indices=True, root_central_atom=root_central_atom, include_hydrogens=include_hydrogens
            )
        else:
            shinglings = DRFPUtil.shingling_from_mol(
                mol, radius=radius, rings=rings, min_radius=min_radius,
                get_atom_indices=False, root_central_atom=root_central_atom, include_hydrogens=include_hydrogens
            )
            atom_indices_map = None

        hash_values = DRFPUtil.hash(shinglings)
        folded, indices = DRFPUtil.fold(hash_values)
        if get_atom_indices:
            return folded, indices, {in_smiles: [atom_indices_map]}
        else:
            return folded, indices

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        # Use a stable hash function (e.g., builtin hash, but mask to 32 bits for numpy)
        return np.array([hash(s) & 0xFFFFFFFF for s in shingling], dtype=np.uint32)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        # Fold by modulo
        indices = hash_values % length
        folded = np.zeros(length, dtype=np.uint8)
        for idx in indices:
            folded[idx] = 1
        return folded, indices

    @staticmethod
    def encode(
        X: Union[Iterable, str],
        n_folded_length: int = 2048,
        min_radius: int = 0,
        radius: int = 3,
        rings: bool = True,
        mapping: bool = False,
        atom_index_mapping: bool = False,
        root_central_atom: bool = True,
        include_hydrogens: bool = False,
        show_progress_bar: bool = False
    ) -> Union[
        List[np.ndarray],
        Tuple[List[np.ndarray], Dict[int, Set[str]]],
        Tuple[List[np.ndarray], Dict[int, Set[str]]],
        List[Dict[str, List[Dict[str, List[Set[int]]]]]]
    ]:
        import sys
        if isinstance(X, str):
            X = [X]
        X = list(X)
        n = len(X)
        results = []
        mapping_dict = {}
        atom_index_maps = []
        if show_progress_bar:
            try:
                from tqdm import tqdm
                iterator = tqdm(X)
            except ImportError:
                iterator = X
        else:
            iterator = X

        for i, smiles in enumerate(iterator):
            try:
                if atom_index_mapping:
                    folded, indices, atom_indices_map = DRFPUtil.internal_encode(
                        smiles, radius=radius, min_radius=min_radius, rings=rings,
                        get_atom_indices=True, root_central_atom=root_central_atom, include_hydrogens=include_hydrogens
                    )
                    atom_index_maps.append(atom_indices_map)
                else:
                    folded, indices = DRFPUtil.internal_encode(
                        smiles, radius=radius, min_radius=min_radius, rings=rings,
                        get_atom_indices=False, root_central_atom=root_central_atom, include_hydrogens=include_hydrogens
                    )
                results.append(folded)
                if mapping:
                    mapping_dict[i] = set(indices)
            except Exception as e:
                results.append(np.zeros(n_folded_length, dtype=np.uint8))
                if mapping:
                    mapping_dict[i] = set()
                if atom_index_mapping:
                    atom_index_maps.append({})
        if atom_index_mapping:
            return atom_index_maps
        elif mapping:
            return results, mapping_dict
        else:
            return results
