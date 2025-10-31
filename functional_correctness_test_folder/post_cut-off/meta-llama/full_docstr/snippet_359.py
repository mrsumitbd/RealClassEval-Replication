
from rdkit import Chem
from rdkit.Chem import AllChem
from typing import List, Tuple, Union, Iterable, Dict, Set
import numpy as np
from tqdm import tqdm


class DRFPUtil:
    '''
    A utility class for encoding SMILES as drfp fingerprints.
    '''

    @staticmethod
    def shingling_from_mol(in_mol: Chem.Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        shingling = set()
        atom_indices = {}
        for atom in in_mol.GetAtoms():
            if not include_hydrogens and atom.GetAtomicNum() == 1:
                continue
            for r in range(min_radius, radius + 1):
                env = Chem.FindAtomEnvironmentOfRadiusN(
                    in_mol, r, atom.GetIdx())
                if env:
                    submol = Chem.PathToSubmol(in_mol, env)
                    if root_central_atom:
                        submol_smiles = Chem.MolToSmiles(
                            submol, rootedAtAtom=atom.GetIdx())
                    else:
                        submol_smiles = Chem.MolToSmiles(submol)
                    shingling.add(submol_smiles)
                    if get_atom_indices:
                        if submol_smiles not in atom_indices:
                            atom_indices[submol_smiles] = []
                        atom_indices[submol_smiles].append(
                            set([atom.GetIdx()]))
        if rings:
            for ring in in_mol.GetRingInfo().AtomRings():
                submol = Chem.PathToSubmol(in_mol, list(ring))
                submol_smiles = Chem.MolToSmiles(submol)
                shingling.add(submol_smiles)
                if get_atom_indices:
                    if submol_smiles not in atom_indices:
                        atom_indices[submol_smiles] = []
                    atom_indices[submol_smiles].append(set(ring))
        shingling = list(shingling)
        if get_atom_indices:
            return shingling, atom_indices
        return shingling

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        reactants, products = in_smiles.split('>>')
        reactants_mol = Chem.MolFromSmiles(reactants)
        products_mol = Chem.MolFromSmiles(products)
        reactants_shingling, reactants_atom_indices = DRFPUtil.shingling_from_mol(
            reactants_mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
        products_shingling, products_atom_indices = DRFPUtil.shingling_from_mol(
            products_mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
        shingling = list(set(reactants_shingling + products_shingling))
        hash_values = DRFPUtil.hash(shingling)
        substructure_smiles = np.array(shingling)
        if get_atom_indices:
            atom_index_mapping = {
                'reactants': reactants_atom_indices, 'products': products_atom_indices}
            return hash_values, substructure_smiles, atom_index_mapping
        return hash_values, substructure_smiles

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        hash_values = np.array(
            [hash(s) & 0xffffffff for s in shingling], dtype=np.uint32)
        return hash_values

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        folded_fingerprint = np.zeros(length, dtype=np.uint8)
        indices = hash_values % length
        folded_fingerprint[indices] = 1
        return folded_fingerprint, indices

    @staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        if isinstance(X, str):
            X = [X]
        fingerprints = []
        feature_to_substructure = {}
        atom_index_mappings = []
        iterator = tqdm(X, desc='Encoding SMILES') if show_progress_bar else X
        for i, smiles in enumerate(iterator):
            if atom_index_mapping:
                hash_values, substructure_smiles, atom_index_mapping = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, True, root_central_atom, include_hydrogens)
                atom_index_mappings.append(atom_index_mapping)
            else:
                hash_values, substructure_smiles = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, False, root_central_atom, include_hydrogens)
            fingerprint, indices = DRFPUtil.fold(hash_values, n_folded_length)
            fingerprints.append(fingerprint)
            if mapping:
                for index, substructure_smile in zip(indices, substructure_smiles):
                    if index not in feature_to_substructure:
                        feature_to_substructure[index] = set()
                    feature_to_substructure[index].add(substructure_smile)
        if mapping and atom_index_mapping:
            return fingerprints, feature_to_substructure, atom_index_mappings
        elif mapping:
            return fingerprints, feature_to_substructure
        elif atom_index_mapping:
            return fingerprints, atom_index_mappings
        return fingerprints
