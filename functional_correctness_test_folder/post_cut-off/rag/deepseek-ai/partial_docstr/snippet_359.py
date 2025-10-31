
import numpy as np
from typing import List, Tuple, Dict, Set, Union, Iterable
from rdkit.Chem import Mol
from collections import defaultdict
import hashlib
from tqdm import tqdm


class DRFPUtil:
    '''
    A utility class for encoding SMILES as drfp fingerprints.
    '''

    @staticmethod
    def shingling_from_mol(in_mol: Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        '''Creates a molecular shingling from a RDKit molecule (rdkit.Chem.rdchem.Mol).'''
        pass

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        '''Creates an drfp array from a reaction SMILES string.'''
        pass

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        '''Directly hash all the SMILES in a shingling to a 32-bit integer.'''
        hashes = []
        for s in shingling:
            h = int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % (2**32)
            hashes.append(h)
        return np.array(hashes, dtype=np.uint32)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        '''Folds the hash values to a binary vector of a given length.'''
        indices = np.unique(hash_values % length)
        folded = np.zeros(length, dtype=np.uint8)
        folded[indices] = 1
        return folded, indices

    @staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        '''Encodes a list of reaction SMILES using the drfp fingerprint.'''
        if isinstance(X, str):
            X = [X]

        fingerprints = []
        feature_mapping = defaultdict(set)
        atom_mappings = []

        iterator = tqdm(X) if show_progress_bar else X

        for smiles in iterator:
            if atom_index_mapping:
                hashes, features, atom_map = DRFPUtil.internal_encode(
                    smiles,
                    radius=radius,
                    min_radius=min_radius,
                    rings=rings,
                    get_atom_indices=True,
                    root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                atom_mappings.append(atom_map)
            else:
                hashes, features = DRFPUtil.internal_encode(
                    smiles,
                    radius=radius,
                    min_radius=min_radius,
                    rings=rings,
                    root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )

            folded, indices = DRFPUtil.fold(hashes, n_folded_length)
            fingerprints.append(folded)

            if mapping:
                for idx in indices:
                    feature_mapping[idx].update(features[idx])

        if mapping and atom_index_mapping:
            return fingerprints, feature_mapping, atom_mappings
        elif mapping:
            return fingerprints, feature_mapping
        elif atom_index_mapping:
            return fingerprints, atom_mappings
        else:
            return fingerprints
