
from typing import List, Union, Tuple, Dict, Set, Iterable
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors


class DRFPUtil:

    @staticmethod
    def shingling_from_mol(in_mol: Chem.Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        shingles = []
        atom_indices_map = {}
        for atom in in_mol.GetAtoms():
            if not include_hydrogens and atom.GetAtomicNum() == 1:
                continue
            for r in range(min_radius, radius + 1):
                env = rdMolDescriptors.EnvironmentFingerprint(
                    in_mol, atom.GetIdx(), r, rings)
                if root_central_atom:
                    env = Chem.RDKFingerprint(in_mol, fromAtoms=[atom.GetIdx(
                    )], radius=r, minPath=1, maxPath=2 * r + 1, rings=rings, useHs=include_hydrogens)
                shingle = Chem.MolToSmiles(env)
                shingles.append(shingle)
                if get_atom_indices:
                    if shingle not in atom_indices_map:
                        atom_indices_map[shingle] = []
                    atom_indices_map[shingle].append(
                        set(env.GetSubstructMatches(Chem.MolFromSmiles(shingle))[0]))
        if get_atom_indices:
            return shingles, atom_indices_map
        return shingles

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]:
        mol = Chem.MolFromSmiles(in_smiles)
        shingles, atom_indices_map = DRFPUtil.shingling_from_mol(mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
        hash_values = DRFPUtil.hash(shingles)
        folded_hash, folded_counts = DRFPUtil.fold(hash_values)
        if get_atom_indices:
            return folded_hash, folded_counts, atom_indices_map
        return folded_hash, folded_counts

    @ staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        return np.array([hash(shingle) for shingle in shingling])

    @ staticmethod
    def fold(hash_values: np.ndarray, length: int=2048) -> Tuple[np.ndarray, np.ndarray]:
        folded_indices = hash_values % length
        counts = np.bincount(folded_indices, minlength=length)
        folded_hash = np.zeros(length, dtype=int)
        np.add.at(folded_hash, folded_indices, 1)
        return folded_hash, counts

    @ staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int=2048, min_radius: int=0, radius: int=3, rings: bool=True, mapping: bool=False, atom_index_mapping: bool=False, root_central_atom: bool=True, include_hydrogens: bool=False, show_progress_bar: bool=False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]:
        if isinstance(X, str):
            X = [X]
        fingerprints = []
        feature_to_substructure_mapping = {}
        atom_indices_maps = []
        for i, smiles in enumerate(X):
            if show_progress_bar:
                print(f"Processing {i+1}/{len(X)}", end='\r')
            if mapping or atom_index_mapping:
                folded_hash, counts, atom_indices_map = DRFPUtil.internal_encode(smiles, radius, min_radius, rings, atom_index_mapping, root_central_atom, include_hydrogens)
                atom_indices_maps.append(atom_indices_map)
            else:
                folded_hash, counts = DRFPUtil.internal_encode(smiles, radius, min_radius, rings, atom_index_mapping, root_central_atom, include_hydrogens)
            fingerprints.append(folded_hash)
            if mapping:
                for shingle, indices in atom_indices_map.items():
                    if shingle not in feature_to_substructure_mapping:
                        feature_to_substructure_mapping[shingle] = set()
                    feature_to_substructure_mapping[shingle].update(indices)
        if show_progress_bar:
            print()
        if mapping:
            return fingerprints, feature_to_substructure_mapping
        if atom_index_mapping:
            return fingerprints, atom_indices_maps
        return fingerprints
