
from typing import List, Union, Tuple, Dict, Set, Iterable
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors


class DRFPUtil:

    @staticmethod
    def shingling_from_mol(in_mol: Chem.Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        shingles = []
        atom_indices_dict = {}
        for atom in in_mol.GetAtoms():
            if not include_hydrogens and atom.GetAtomicNum() == 1:
                continue
            for r in range(min_radius, radius + 1):
                env = rdMolDescriptors.EnvironmentFingerprint(
                    in_mol, atom.GetIdx(), r, rings)
                shingle = env.GetNonzeroElements().keys()
                shingle_str = ','.join(sorted(map(str, shingle)))
                if root_central_atom:
                    shingle_str = f"{atom.GetIdx()}:{shingle_str}"
                shingles.append(shingle_str)
                if get_atom_indices:
                    if shingle_str not in atom_indices_dict:
                        atom_indices_dict[shingle_str] = []
                    atom_indices_dict[shingle_str].append({atom.GetIdx()})
        if get_atom_indices:
            return shingles, atom_indices_dict
        return shingles

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        in_mol = Chem.MolFromSmiles(in_smiles)
        shingles, atom_indices_dict = DRFPUtil.shingling_from_mol(
            in_mol, radius, rings, min_radius, True, root_central_atom, include_hydrogens)
        hash_values = DRFPUtil.hash(shingles)
        folded_hash, folded_counts = DRFPUtil.fold(hash_values)
        if get_atom_indices:
            return folded_hash, folded_counts, atom_indices_dict
        return folded_hash, folded_counts

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        hash_values = np.array([hash(shingle)
                               for shingle in shingling], dtype=np.int64)
        return hash_values

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        folded_hash = np.zeros(length, dtype=np.int64)
        folded_counts = np.zeros(length, dtype=np.int64)
        for hash_value in hash_values:
            index = hash_value % length
            folded_hash[index] ^= hash_value
            folded_counts[index] += 1
        return folded_hash, folded_counts

    @staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        if isinstance(X, str):
            X = [X]
        encoded_list = []
        atom_index_mapping_dict = {}
        for i, smiles in enumerate(X):
            if show_progress_bar:
                print(f"Processing {i+1}/{len(X)}", end='\r')
            folded_hash, folded_counts, atom_indices_dict = DRFPUtil.internal_encode(
                smiles, radius, min_radius, rings, True, root_central_atom, include_hydrogens)
            encoded_list.append(folded_hash)
            if atom_index_mapping:
                atom_index_mapping_dict[i] = atom_indices_dict
        if show_progress_bar:
            print()
        if mapping:
            return encoded_list, atom_index_mapping_dict
        return encoded_list
