
from typing import Union, List, Tuple, Dict, Set, Iterable
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
import numpy as np
from collections import defaultdict


class DRFPUtil:

    @staticmethod
    def shingling_from_mol(in_mol: Chem.Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        if not in_mol:
            return [] if not get_atom_indices else ([], {})

        if not include_hydrogens:
            in_mol = Chem.RemoveHs(in_mol)

        shingling = []
        atom_indices_dict = defaultdict(list)

        for atom in in_mol.GetAtoms():
            if root_central_atom:
                env = rdMolDescriptors.FindAtomEnvironmentOfRadiusN(
                    in_mol, radius, atom.GetIdx())
                submol = Chem.PathToSubmol(in_mol, env)
                if submol:
                    smi = Chem.MolToSmiles(
                        submol, rootedAtAtom=atom.GetIdx(), canonical=True)
                    shingling.append(smi)
                    if get_atom_indices:
                        atom_indices_dict[smi].append({atom.GetIdx()})
            else:
                for r in range(min_radius, radius + 1):
                    env = rdMolDescriptors.FindAtomEnvironmentOfRadiusN(
                        in_mol, r, atom.GetIdx())
                    submol = Chem.PathToSubmol(in_mol, env)
                    if submol:
                        smi = Chem.MolToSmiles(submol, canonical=True)
                        shingling.append(smi)
                        if get_atom_indices:
                            atom_indices_dict[smi].append({atom.GetIdx()})

        if rings and rings is not False:
            ri = in_mol.GetRingInfo()
            for ring in ri.AtomRings():
                env = set()
                for atom_idx in ring:
                    env.update(rdMolDescriptors.FindAtomEnvironmentOfRadiusN(
                        in_mol, 0, atom_idx))
                submol = Chem.PathToSubmol(in_mol, env)
                if submol:
                    smi = Chem.MolToSmiles(submol, canonical=True)
                    shingling.append(smi)
                    if get_atom_indices:
                        atom_indices_dict[smi].append(set(ring))

        if not get_atom_indices:
            return shingling
        else:
            return shingling, atom_indices_dict

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        mol = Chem.MolFromSmiles(in_smiles)
        if not mol:
            return (np.array([]), np.array([])) if not get_atom_indices else (np.array([]), np.array([]), {})

        result = DRFPUtil.shingling_from_mol(
            mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)

        if not get_atom_indices:
            shingling = result
            hashed = DRFPUtil.hash(shingling)
            folded = DRFPUtil.fold(hashed)
            return folded
        else:
            shingling, atom_indices = result
            hashed = DRFPUtil.hash(shingling)
            folded = DRFPUtil.fold(hashed)
            return folded[0], folded[1], atom_indices

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        if not shingling:
            return np.array([])
        hashes = [hash(s) & 0xffffffff for s in shingling]
        return np.array(hashes, dtype=np.uint32)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        if len(hash_values) == 0:
            return (np.zeros(length, dtype=np.uint8), np.zeros(length, dtype=np.uint8))

        folded = np.zeros(length, dtype=np.uint8)
        folded_hashes = np.zeros(length, dtype=np.uint32)

        for h in hash_values:
            idx = h % length
            folded[idx] = 1
            folded_hashes[idx] = h

        return (folded, folded_hashes)

    @staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        if isinstance(X, str):
            X = [X]

        fingerprints = []
        feature_mapping = defaultdict(set)
        atom_mappings = []

        for smiles in X:
            result = DRFPUtil.internal_encode(
                smiles, radius, min_radius, rings, atom_index_mapping, root_central_atom, include_hydrogens)

            if not atom_index_mapping:
                folded, folded_hashes = result
                fingerprints.append(folded)
                if mapping:
                    for h in folded_hashes:
                        if h != 0:
                            feature_mapping[h % n_folded_length].add(smiles)
            else:
                folded, folded_hashes, atom_indices = result
                fingerprints.append(folded)
                if mapping:
                    for h in folded_hashes:
                        if h != 0:
                            feature_mapping[h % n_folded_length].add(smiles)
                atom_mappings.append(atom_indices)

        if mapping and not atom_index_mapping:
            return fingerprints, feature_mapping
        elif mapping and atom_index_mapping:
            return fingerprints, feature_mapping, atom_mappings
        elif atom_index_mapping:
            return fingerprints, atom_mappings
        else:
            return fingerprints
