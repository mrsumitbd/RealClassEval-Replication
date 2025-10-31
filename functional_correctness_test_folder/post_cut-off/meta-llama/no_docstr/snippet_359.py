
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np
from typing import List, Tuple, Union, Iterable, Dict, Set
from tqdm import tqdm


class DRFPUtil:

    @staticmethod
    def shingling_from_mol(in_mol: Chem.Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        shingling = []
        atom_indices = {}
        for atom_idx in range(in_mol.GetNumAtoms()):
            if not include_hydrogens and in_mol.GetAtomWithIdx(atom_idx).GetAtomicNum() == 1:
                continue
            atom_env = AllChem.FindAtomEnvironmentOfRadiusN(
                in_mol, radius, atom_idx, useHs=include_hydrogens)
            if not atom_env:
                continue
            if root_central_atom:
                atom_env.add(atom_idx)
            submol = Chem.PathToSubmol(in_mol, atom_env)
            try:
                shingling.append(Chem.MolToSmiles(submol))
            except:
                continue
            if get_atom_indices:
                if shingling[-1] not in atom_indices:
                    atom_indices[shingling[-1]] = []
                atom_indices[shingling[-1]].append(set([i for i in atom_env]))
        if rings:
            for ring in in_mol.GetRingInfo().AtomRings():
                if min_radius <= len(ring) <= radius*2+1:
                    submol = Chem.PathToSubmol(in_mol, ring)
                    try:
                        shingling.append(Chem.MolToSmiles(submol))
                    except:
                        continue
                    if get_atom_indices:
                        if shingling[-1] not in atom_indices:
                            atom_indices[shingling[-1]] = []
                        atom_indices[shingling[-1]].append(set(ring))
        if get_atom_indices:
            return shingling, atom_indices
        else:
            return shingling

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        mol = Chem.MolFromSmiles(in_smiles)
        if mol is None:
            return np.array([]), np.array([])
        shingling = DRFPUtil.shingling_from_mol(mol, radius=radius, rings=rings, min_radius=min_radius,
                                                get_atom_indices=get_atom_indices, root_central_atom=root_central_atom, include_hydrogens=include_hydrogens)
        if get_atom_indices:
            shingling, atom_indices = shingling
        else:
            atom_indices = None
        hash_values = DRFPUtil.hash(shingling)
        folded, min_hash = DRFPUtil.fold(hash_values)
        if get_atom_indices:
            return folded, min_hash, atom_indices
        else:
            return folded, min_hash

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        return np.array([hash(s) % (2**32) for s in shingling], dtype=np.uint32)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        min_hash = np.min(hash_values)
        folded = np.zeros(length, dtype=np.uint32)
        for hv in hash_values:
            folded[hv % length] = 1
        return folded, np.array([min_hash], dtype=np.uint32)

    @staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        if isinstance(X, str):
            X = [X]
        results = []
        atom_index_mappings = {}
        for i, smiles in tqdm(enumerate(X), desc="Encoding SMILES", disable=not show_progress_bar):
            if atom_index_mapping:
                folded, min_hash, atom_indices = DRFPUtil.internal_encode(
                    smiles, radius=radius, min_radius=min_radius, rings=rings, get_atom_indices=True, root_central_atom=root_central_atom, include_hydrogens=include_hydrogens)
                results.append(np.concatenate((folded, min_hash)))
                atom_index_mappings[i] = atom_indices
            else:
                folded, min_hash = DRFPUtil.internal_encode(smiles, radius=radius, min_radius=min_radius, rings=rings,
                                                            get_atom_indices=False, root_central_atom=root_central_atom, include_hydrogens=include_hydrogens)
                results.append(np.concatenate((folded, min_hash)))
        if mapping:
            if atom_index_mapping:
                return results, atom_index_mappings
            else:
                # Create a dummy atom_index_mappings to satisfy the type hint
                atom_index_mappings = {i: set() for i in range(len(X))}
                return results, atom_index_mappings
        else:
            return results
