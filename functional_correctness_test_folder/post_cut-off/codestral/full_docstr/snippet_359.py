
import numpy as np
from typing import List, Tuple, Union, Dict, Set, Iterable
from rdkit.Chem.rdchem import Mol
from rdkit import Chem
from rdkit.Chem import AllChem
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
        atom_indices_mapping = {}

        for atom in in_mol.GetAtoms():
            for r in range(min_radius, radius + 1):
                env = Chem.FindAtomEnvironmentOfRadiusN(
                    in_mol, r, atom.GetIdx())
                submol = Chem.PathToSubmol(in_mol, env)
                if submol is not None:
                    smiles = Chem.MolToSmiles(submol, rootedAtAtom=atom.GetIdx(
                    ) if root_central_atom else -1, isomericSmiles=False, canonical=False)
                    if smiles not in shingling:
                        shingling.append(smiles)
                        if get_atom_indices:
                            atom_indices_mapping[smiles] = [set(env)]
                    elif get_atom_indices:
                        atom_indices_mapping[smiles].append(set(env))

        if rings:
            ssr = Chem.GetSymmSSSR(in_mol)
            for ring in ssr:
                submol = Chem.PathToSubmol(in_mol, ring)
                if submol is not None:
                    smiles = Chem.MolToSmiles(
                        submol, isomericSmiles=False, canonical=False)
                    if smiles not in shingling:
                        shingling.append(smiles)
                        if get_atom_indices:
                            atom_indices_mapping[smiles] = [set(ring)]
                    elif get_atom_indices:
                        atom_indices_mapping[smiles].append(set(ring))

        if get_atom_indices:
            return shingling, atom_indices_mapping
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
        reactants, products = in_smiles.split('>>')
        reactant_mols = [Chem.MolFromSmiles(smiles)
                         for smiles in reactants.split('.')]
        product_mols = [Chem.MolFromSmiles(smiles)
                        for smiles in products.split('.')]

        shingling = []
        atom_indices_mapping = {}

        for mol in reactant_mols + product_mols:
            if mol is not None:
                if get_atom_indices:
                    mol_shingling, mol_atom_indices_mapping = DRFPUtil.shingling_from_mol(
                        mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
                    shingling.extend(mol_shingling)
                    atom_indices_mapping.update(mol_atom_indices_mapping)
                else:
                    shingling.extend(DRFPUtil.shingling_from_mol(
                        mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens))

        hash_values = DRFPUtil.hash(shingling)
        if get_atom_indices:
            return hash_values, np.array(shingling), atom_indices_mapping
        else:
            return hash_values, np.array(shingling)

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        '''Directly hash all the SMILES in a shingling to a 32-bit integer.
        Arguments:
            shingling: A list of n-grams
        Returns:
            A list of hashed n-grams
        '''
        return np.array([hash(smiles) for smiles in shingling], dtype=np.uint32)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        '''Folds the hash values to a binary vector of a given length.
        Arguments:
            hash_value: An array containing the hash values
            length: The length of the folded fingerprint
        Returns:
            A tuple containing the folded fingerprint and the indices of the on bits
        '''
        folded = np.zeros(length, dtype=np.uint8)
        on_bits = np.unique(hash_values % length)
        folded[on_bits] = 1
        return folded, on_bits

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
        feature_mapping = {}
        atom_indices_mappings = []

        for i, smiles in enumerate(tqdm(X, disable=not show_progress_bar)):
            if atom_index_mapping:
                hash_values, substructures, atom_indices_mapping = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, atom_index_mapping, root_central_atom, include_hydrogens)
                atom_indices_mappings.append(atom_indices_mapping)
            else:
                hash_values, substructures = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, atom_index_mapping, root_central_atom, include_hydrogens)

            folded, on_bits = DRFPUtil.fold(hash_values, n_folded_length)
            fingerprints.append(folded)

            if mapping:
                feature_mapping[i] = set(substructures[on_bits])

        if mapping and atom_index_mapping:
            return fingerprints, feature_mapping, atom_indices_mappings
        elif mapping:
            return fingerprints, feature_mapping
        elif atom_index_mapping:
            return fingerprints, atom_indices_mappings
        else:
            return fingerprints
