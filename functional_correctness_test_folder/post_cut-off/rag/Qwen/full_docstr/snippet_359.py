
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from typing import List, Union, Tuple, Dict, Set, Iterable
import numpy as np
from tqdm import tqdm


class DRFPUtil:
    '''
    A utility class for encoding SMILES as drfp fingerprints.
    '''
    @staticmethod
    def shingling_from_mol(in_mol: Chem.Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        '''Creates a molecular shingling from a RDKit molecule (rdkit.Chem.rdchem.Mol).
        Arguments:
            in_mol: A RDKit molecule instance
            radius: The drfp radius (a radius of 3 corresponds to drfp6)
            rings: Whether or not to include rings in the shingling
            min_radius: The minimum radius that is used to extract n-grams
        Returns:
            The molecular shingling.
        '''
        shingling = []
        atom_indices_dict = {}
        for atom in in_mol.GetAtoms():
            atom_idx = atom.GetIdx()
            envs = rdMolDescriptors.RDKit2D.MolGetAtomEnvironment(
                in_mol, radius, atom_idx, includeHs=include_hydrogens)
            for r in range(min_radius, radius + 1):
                for env in envs:
                    if len(env) == r:
                        submol = Chem.PathToSubmol(
                            in_mol, env, useBonds=True, rootedAtAtom=atom_idx if root_central_atom else -1)
                        subsmiles = Chem.MolToSmiles(
                            submol, rootedAtAtom=atom_idx if root_central_atom else -1)
                        if rings or not any(subsmiles.count(x) > 1 for x in '()'):
                            shingling.append(subsmiles)
                            if get_atom_indices:
                                if subsmiles not in atom_indices_dict:
                                    atom_indices_dict[subsmiles] = []
                                atom_indices_dict[subsmiles].append(set(env))
        if get_atom_indices:
            return shingling, atom_indices_dict
        return shingling

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]:
        '''Creates an drfp array from a reaction SMILES string.
        Arguments:
            in_smiles: A valid reaction SMILES string
            radius: The drfp radius (a radius of 3 corresponds to drfp6)
            min_radius: The minimum radius that is used to extract n-grams
            rings: Whether or not to include rings in the shingling
        Returns:
            A tuple with two arrays, the first containing the drfp hash values, the second the substructure SMILES
        '''
        mol = Chem.MolFromSmiles(in_smiles)
        if mol is None:
            raise ValueError("Invalid SMILES string")
        shingling, atom_indices_dict = DRFPUtil.shingling_from_mol(mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
        hash_values = DRFPUtil.hash(shingling)
        if get_atom_indices:
            return hash_values, np.array(shingling), atom_indices_dict
        return hash_values, np.array(shingling)

    @ staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        '''Directly hash all the SMILES in a shingling to a 32-bit integer.
        Arguments:
            shingling: A list of n-grams
        Returns:
            A list of hashed n-grams
        '''
        return np.array([hash(s) & 0xFFFFFFFF for s in shingling], dtype=np.uint32)

    @ staticmethod
    def fold(hash_values: np.ndarray, length: int=2048) -> Tuple[np.ndarray, np.ndarray]:
        '''Folds the hash values to a binary vector of a given length.
        Arguments:
            hash_values: An array containing the hash values
            length: The length of the folded fingerprint
        Returns:
            A tuple containing the folded fingerprint and the indices of the on bits
        '''
        folded = np.zeros(length, dtype=np.uint8)
        indices = hash_values % length
        folded[indices] = 1
        return folded, indices

    @ staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int=2048, min_radius: int=0, radius: int=3, rings: bool=True, mapping: bool=False, atom_index_mapping: bool=False, root_central_atom: bool=True, include_hydrogens: bool=False, show_progress_bar: bool=False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]:
        '''Encodes a list of reaction SMILES using the drfp fingerprint.
        Args:
            X: An iterable (e.g. List) of reaction SMILES or a single reaction SMILES to be encoded
            n_folded_length: The folded length of the fingerprint (the parameter for the modulo hashing)
            min_radius: The minimum radius of a substructure (0 includes single atoms)
            radius: The maximum radius of a substructure
            rings: Whether to include full rings as substructures
            mapping: Return a feature to substructure mapping in addition to the fingerprints
            atom_index_mapping: Return the atom indices of mapped substructures for each reaction
            root_central_atom: Whether to root the central atom of substructures when generating SMILES
            show_progress_bar: Whether to show a progress bar when encoding reactions
        Returns:
            A list of drfp fingerprints or, if mapping is enabled, a tuple containing a list of drfp fingerprints and a mapping dict.
        '''
        if isinstance(X, str):
            X = [X]
        fingerprints = []
        substructure_mapping = {}
        atom_indices_mapping = {}
        iterable = tqdm(X) if show_progress_bar else X
        for idx, smiles in enumerate(iterable):
            if atom_index_mapping:
                hash_values, substructures, atom_indices_dict = DRFPUtil.internal_encode(smiles, radius, min_radius, rings, True, root_central_atom, include_hydrogens)
                atom_indices_mapping[idx] = atom_indices_dict
            else:
                hash_values, substructures = DRFPUtil.internal_encode(smiles, radius, min_radius, rings, False, root_central_atom, include_hydrogens)
            folded_fingerprint, _ = DRFPUtil.fold(hash_values, n_folded_length)
            fingerprints.append(folded_fingerprint)
            if mapping:
                for substructure in substructures:
                    if substructure not in substructure_mapping:
                        substructure_mapping[substructure] = set()
                    substructure_mapping[substructure].add(idx)
        if mapping and atom_index_mapping:
            return fingerprints, substructure_mapping, atom_indices_mapping
        elif mapping:
            return fingerprints, substructure_mapping
        elif atom_index_mapping:
            return fingerprints, atom_indices_mapping
        return fingerprints
