
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np
from typing import List, Tuple, Union, Iterable, Dict, Set
from tqdm import tqdm


class DRFPUtil:
    '''
    A utility class for encoding SMILES as drfp fingerprints.
    '''

    @staticmethod
    def shingling_from_mol(in_mol: Chem.Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        '''
        Creates a molecular shingling from a RDKit molecule (rdkit.Chem.rdchem.Mol).
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
                if env is not None:
                    submol = Chem.PathToSubmol(in_mol, env)
                    if root_central_atom:
                        smi = Chem.MolToSmiles(
                            submol, rootedAtAtom=atom.GetIdx())
                    else:
                        smi = Chem.MolToSmiles(submol)
                    shingling.append(smi)
                    if get_atom_indices:
                        atom_idx_set = set(
                            [atom.GetIdx()] + [a.GetIdx() for a in submol.GetAtoms()])
                        if smi not in atom_indices:
                            atom_indices[smi] = []
                        atom_indices[smi].append(atom_idx_set)
        if rings:
            for ring in in_mol.GetRingInfo().AtomRings():
                submol = Chem.PathToSubmol(in_mol, list(ring))
                smi = Chem.MolToSmiles(submol)
                shingling.append(smi)
                if get_atom_indices:
                    atom_idx_set = set(ring)
                    if smi not in atom_indices:
                        atom_indices[smi] = []
                    atom_indices[smi].append(atom_idx_set)
        if get_atom_indices:
            return shingling, atom_indices
        else:
            return shingling

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        '''
        Creates an drfp array from a reaction SMILES string.
        Arguments:
            in_smiles: A valid reaction SMILES string
            radius: The drfp radius (a radius of 3 corresponds to drfp6)
            min_radius: The minimum radius that is used to extract n-grams
            rings: Whether or not to include rings in the shingling
        Returns:
            A tuple with two arrays, the first containing the drfp hash values, the second the substructure SMILES
        '''
        reactants, products = in_smiles.split('>>')
        reactant_mols = [Chem.MolFromSmiles(smi)
                         for smi in reactants.split('.')]
        product_mols = [Chem.MolFromSmiles(smi) for smi in products.split('.')]
        reactant_shingling = []
        product_shingling = []
        reactant_atom_indices = {}
        product_atom_indices = {}
        for mol in reactant_mols:
            shingling = DRFPUtil.shingling_from_mol(
                mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
            if get_atom_indices:
                reactant_shingling.extend(shingling[0])
                for smi, indices in shingling[1].items():
                    if smi not in reactant_atom_indices:
                        reactant_atom_indices[smi] = []
                    reactant_atom_indices[smi].extend(indices)
            else:
                reactant_shingling.extend(shingling)
        for mol in product_mols:
            shingling = DRFPUtil.shingling_from_mol(
                mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
            if get_atom_indices:
                product_shingling.extend(shingling[0])
                for smi, indices in shingling[1].items():
                    if smi not in product_atom_indices:
                        product_atom_indices[smi] = []
                    product_atom_indices[smi].extend(indices)
            else:
                product_shingling.extend(shingling)
        shingling = list(set(reactant_shingling + product_shingling))
        hash_values = DRFPUtil.hash(shingling)
        if get_atom_indices:
            atom_index_mapping = {
                'reactants': reactant_atom_indices, 'products': product_atom_indices}
            return hash_values, np.array(shingling), atom_index_mapping
        else:
            return hash_values, np.array(shingling)

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        '''
        Directly hash all the SMILES in a shingling to a 32-bit integer.
        Arguments:
            shingling: A list of n-grams
        Returns:
            A list of hashed n-grams
        '''
        return np.array([hash(smi) % (2**32) for smi in shingling], dtype=np.uint32)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        '''
        Folds the hash values to a binary vector of a given length.
        Arguments:
            hash_value: An array containing the hash values
            length: The length of the folded fingerprint
        Returns:
            A tuple containing the folded fingerprint and the indices of the on bits
        '''
        folded_fingerprint = np.zeros(length, dtype=np.uint8)
        indices = hash_values % length
        folded_fingerprint[indices] = 1
        return folded_fingerprint, indices

    @staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        '''
        Encodes a list of reaction SMILES using the drfp fingerprint.
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
        mappings = []
        atom_index_mappings = []
        for smiles in tqdm(X, desc='Encoding SMILES', disable=not show_progress_bar):
            if atom_index_mapping:
                hash_values, shingling, atom_indices = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, True, root_central_atom, include_hydrogens)
                atom_index_mappings.append(atom_indices)
            else:
                hash_values, shingling = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, False, root_central_atom, include_hydrogens)
            folded_fingerprint, indices = DRFPUtil.fold(
                hash_values, n_folded_length)
            fingerprints.append(folded_fingerprint)
            if mapping:
                smi_dict = {i: set() for i in indices}
                for i, smi in zip(hash_values, shingling):
                    smi_dict[i % n_folded_length].add(smi)
                mappings.append(smi_dict)
        if mapping and atom_index_mapping:
            return fingerprints, mappings, atom_index_mappings
        elif mapping:
            return fingerprints, mappings
        elif atom_index_mapping:
            return fingerprints, atom_index_mappings
        else:
            return fingerprints
