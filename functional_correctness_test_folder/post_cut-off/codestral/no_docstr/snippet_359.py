
import numpy as np
from typing import List, Set, Dict, Tuple, Union, Iterable
from rdkit import Chem
from rdkit.Chem import Mol
from tqdm import tqdm


class DRFPUtil:

    @staticmethod
    def shingling_from_mol(in_mol: Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        from rdkit.Chem import AllChem
        from rdkit.Chem import rdmolops

        if not include_hydrogens:
            in_mol = Chem.RemoveHs(in_mol)

        shingles = []
        atom_indices_dict = {}

        for atom in in_mol.GetAtoms():
            if atom.GetAtomicNum() == 1 and not include_hydrogens:
                continue

            for r in range(min_radius, radius + 1):
                env = Chem.FindAtomEnvironmentOfRadiusN(
                    in_mol, r, atom.GetIdx())
                amap = {}
                submol = Chem.PathToSubmol(in_mol, env, atomMap=amap)

                if rings and not rdmolops.ContainsRing(submol):
                    continue

                if root_central_atom:
                    submol = Chem.RenumberAtoms(submol, list(amap.values()))

                smiles = Chem.MolToSmiles(
                    submol, isomericSmiles=True, canonical=True)
                shingles.append(smiles)

                if get_atom_indices:
                    atom_indices = set(amap.values())
                    if smiles not in atom_indices_dict:
                        atom_indices_dict[smiles] = []
                    atom_indices_dict[smiles].append(atom_indices)

        if get_atom_indices:
            return shingles, atom_indices_dict
        else:
            return shingles

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        from rdkit.Chem import AllChem

        mol = Chem.MolFromSmiles(in_smiles)
        if mol is None:
            raise ValueError(f"Invalid SMILES string: {in_smiles}")

        if get_atom_indices:
            shingles, atom_indices_dict = DRFPUtil.shingling_from_mol(
                mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
        else:
            shingles = DRFPUtil.shingling_from_mol(
                mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)

        hash_values = DRFPUtil.hash(shingles)
        folded_hash_values, folded_indices = DRFPUtil.fold(hash_values)

        if get_atom_indices:
            return folded_hash_values, folded_indices, atom_indices_dict
        else:
            return folded_hash_values, folded_indices

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        import hashlib

        hash_values = []
        for shingle in shingling:
            hash_object = hashlib.sha256(shingle.encode())
            hash_hex = hash_object.hexdigest()
            hash_int = int(hash_hex, 16)
            hash_values.append(hash_int)

        return np.array(hash_values, dtype=np.uint64)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        folded_hash_values = np.zeros(length, dtype=np.uint64)
        folded_indices = np.zeros(length, dtype=np.uint64)

        for hash_value in hash_values:
            index = hash_value % length
            folded_hash_values[index] += hash_value
            folded_indices[index] += 1

        return folded_hash_values, folded_indices

    @staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        if isinstance(X, str):
            X = [X]

        folded_hash_values_list = []
        mapping_dict = {}
        atom_index_mapping_list = []

        for i, smiles in enumerate(tqdm(X, disable=not show_progress_bar)):
            if atom_index_mapping:
                folded_hash_values, folded_indices, atom_indices_dict = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, True, root_central_atom, include_hydrogens)
                atom_index_mapping_list.append(atom_indices_dict)
            else:
                folded_hash_values, folded_indices = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, False, root_central_atom, include_hydrogens)

            folded_hash_values_list.append(folded_hash_values)

            if mapping:
                unique_shingles = set(DRFPUtil.shingling_from_mol(Chem.MolFromSmiles(
                    smiles), radius, rings, min_radius, False, root_central_atom, include_hydrogens))
                mapping_dict[i] = unique_shingles

        if mapping and atom_index_mapping:
            return folded_hash_values_list, mapping_dict, atom_index_mapping_list
        elif mapping:
            return folded_hash_values_list, mapping_dict
        elif atom_index_mapping:
            return folded_hash_values_list, atom_index_mapping_list
        else:
            return folded_hash_values_list
