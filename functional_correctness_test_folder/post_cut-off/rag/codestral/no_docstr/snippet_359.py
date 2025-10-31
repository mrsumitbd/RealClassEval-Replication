
import numpy as np
from typing import Union, List, Tuple, Dict, Set, Iterable
from rdkit.Chem import Mol
from rdkit.Chem.rdchem import Mol
from rdkit.Chem import AllChem
from rdkit.Chem import rdmolops
from rdkit.Chem import rdChemReactions
from rdkit import Chem
from tqdm import tqdm


class DRFPUtil:
    '''
    A utility class for encoding SMILES as drfp fingerprints.
    '''

    @staticmethod
    def shingling_from_mol(in_mol: Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
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
        atom_indices = {}
        for atom in in_mol.GetAtoms():
            if not include_hydrogens and atom.GetAtomicNum() == 1:
                continue
            for r in range(min_radius, radius + 1):
                env = Chem.FindAtomEnvironmentOfRadiusN(
                    in_mol, r, atom.GetIdx())
                atoms = set()
                for b in env:
                    begin_atom_idx = in_mol.GetBondWithIdx(b).GetBeginAtomIdx()
                    end_atom_idx = in_mol.GetBondWithIdx(b).GetEndAtomIdx()
                    atoms.add(begin_atom_idx)
                    atoms.add(end_atom_idx)
                submol = Chem.PathToSubmol(in_mol, env)
                if root_central_atom:
                    submol = Chem.RDKFingerprint(
                        submol, minPath=1, maxPath=r, fpSize=2048, bitInfo={})
                smiles = Chem.MolToSmiles(submol)
                shingling.append(smiles)
                if get_atom_indices:
                    atom_indices[smiles] = [atoms]
        if rings:
            ssr = Chem.GetSymmSSSR(in_mol)
            for ring in ssr:
                submol = Chem.PathToSubmol(in_mol, ring)
                if root_central_atom:
                    submol = Chem.RDKFingerprint(
                        submol, minPath=1, maxPath=len(ring), fpSize=2048, bitInfo={})
                smiles = Chem.MolToSmiles(submol)
                shingling.append(smiles)
                if get_atom_indices:
                    atom_indices[smiles] = [set(ring)]
        if get_atom_indices:
            return shingling, atom_indices
        else:
            return shingling

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        '''Creates an drfp array from a reaction SMILES string.
        Arguments:
            in_smiles: A valid reaction SMILES string
            radius: The drfp radius (a radius of 3 corresponds to drfp6)
            min_radius: The minimum radius that is used to extract n-grams
            rings: Whether or not to include rings in the shingling
        Returns:
            A tuple with two arrays, the first containing the drfp hash values, the second the substructure SMILES
        '''
        rxn = AllChem.ReactionFromSmarts(in_smiles, useSmiles=True)
        products = rxn.RunReactants((Chem.MolFromSmiles(s)
                                    for s in in_smiles.split('>')[1].split('.')))
        shinglings = []
        atom_indices = {}
        for product in products:
            for mol in product:
                if get_atom_indices:
                    shingling, indices = DRFPUtil.shingling_from_mol(
                        mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
                    shinglings.extend(shingling)
                    atom_indices.update(indices)
                else:
                    shingling = DRFPUtil.shingling_from_mol(
                        mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
                    shinglings.extend(shingling)
        if get_atom_indices:
            return DRFPUtil.hash(shinglings), np.array(shinglings), atom_indices
        else:
            return DRFPUtil.hash(shinglings), np.array(shinglings)

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        '''Directly hash all the SMILES in a shingling to a 32-bit integer.
        Arguments:
            shingling: A list of n-grams
        Returns:
            A list of hashed n-grams
        '''
        return np.array([hash(s) % 2**32 for s in shingling])

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        '''Folds the hash values to a binary vector of a given length.
        Arguments:
            hash_value: An array containing the hash values
            length: The length of the folded fingerprint
        Returns:
            A tuple containing the folded fingerprint and the indices of the on bits
        '''
        folded = np.zeros(length, dtype=np.int8)
        indices = np.unique(hash_values % length)
        folded[indices] = 1
        return folded, indices

    @staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]]:
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
        mapping_dict = {}
        atom_index_dict = {}
        for i, smiles in enumerate(tqdm(X, disable=not show_progress_bar)):
            if atom_index_mapping:
                hash_values, substructures, atom_indices = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, True, root_central_atom, include_hydrogens)
                atom_index_dict[i] = atom_indices
            else:
                hash_values, substructures = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, False, root_central_atom, include_hydrogens)
            folded, indices = DRFPUtil.fold(hash_values, n_folded_length)
            fingerprints.append(folded)
            if mapping:
                mapping_dict[i] = set(substructures[indices])
        if mapping and atom_index_mapping:
            return fingerprints, mapping_dict, atom_index_dict
        elif mapping:
            return fingerprints, mapping_dict
        elif atom_index_mapping:
            return fingerprints, atom_index_dict
        else:
            return fingerprints
