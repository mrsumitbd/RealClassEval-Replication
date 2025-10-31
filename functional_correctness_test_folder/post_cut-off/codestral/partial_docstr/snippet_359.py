
import numpy as np
from typing import List, Tuple, Dict, Set, Union, Iterable
from rdkit import Chem
from rdkit.Chem import Mol
from tqdm import tqdm


class DRFPUtil:

    @staticmethod
    def shingling_from_mol(in_mol: Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        from rdkit.Chem import AllChem
        from rdkit.Chem.Scaffolds import MurckoScaffold

        if not include_hydrogens:
            in_mol = Chem.RemoveHs(in_mol)

        shingles = []
        atom_indices = {}

        for atom in in_mol.GetAtoms():
            for r in range(min_radius, radius + 1):
                env = Chem.FindAtomEnvironmentOfRadiusN(
                    in_mol, r, atom.GetIdx())
                amap = {}
                submol = Chem.PathToSubmol(in_mol, env, atomMap=amap)
                if root_central_atom:
                    submol = Chem.RenumberAtoms(submol, list(amap.values()))
                smi = Chem.MolToSmiles(submol, isomericSmiles=True)
                if smi not in shingles:
                    shingles.append(smi)
                    if get_atom_indices:
                        atom_indices[smi] = [set(amap.values())]

        if rings:
            scaffold = MurckoScaffold.GetScaffoldForMol(in_mol)
            ssr = Chem.GetSymmSSSR(scaffold)
            for ring in ssr:
                ring_atoms = set(ring)
                env = Chem.FindAtomEnvironmentOfRadiusN(
                    in_mol, radius, list(ring_atoms)[0])
                amap = {}
                submol = Chem.PathToSubmol(in_mol, env, atomMap=amap)
                if root_central_atom:
                    submol = Chem.RenumberAtoms(submol, list(amap.values()))
                smi = Chem.MolToSmiles(submol, isomericSmiles=True)
                if smi not in shingles:
                    shingles.append(smi)
                    if get_atom_indices:
                        atom_indices[smi] = [set(amap.values())]

        if get_atom_indices:
            return shingles, atom_indices
        else:
            return shingles

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        from rdkit.Chem import AllChem

        mol = Chem.MolFromSmiles(in_smiles)
        if mol is None:
            raise ValueError(f"Invalid SMILES: {in_smiles}")

        if get_atom_indices:
            shingles, atom_indices = DRFPUtil.shingling_from_mol(
                mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
            hashed = DRFPUtil.hash(shingles)
            folded, counts = DRFPUtil.fold(hashed)
            return folded, counts, atom_indices
        else:
            shingles = DRFPUtil.shingling_from_mol(
                mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
            hashed = DRFPUtil.hash(shingles)
            folded, counts = DRFPUtil.fold(hashed)
            return folded, counts

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        import hashlib

        hashed = []
        for s in shingling:
            hashed.append(
                int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16))
        return np.array(hashed, dtype=np.uint64)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        folded = np.zeros(length, dtype=np.uint8)
        counts = np.zeros(length, dtype=np.uint8)

        for h in hash_values:
            idx = h % length
            folded[idx] = 1
            counts[idx] += 1

        return folded, counts

    @staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        if isinstance(X, str):
            X = [X]

        fingerprints = []
        mapping_dict = {}
        atom_index_mapping_dict = {}

        iterable = tqdm(
            X, desc="Encoding reactions") if show_progress_bar else X

        for i, smiles in enumerate(iterable):
            if atom_index_mapping:
                folded, counts, atom_indices = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, atom_index_mapping, root_central_atom, include_hydrogens)
                atom_index_mapping_dict[i] = atom_indices
            else:
                folded, counts = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, atom_index_mapping, root_central_atom, include_hydrogens)

            fingerprints.append(folded)

            if mapping:
                mapping_dict[i] = set()
                for j, s in enumerate(DRFPUtil.shingling_from_mol(Chem.MolFromSmiles(smiles), radius, rings, min_radius, False, root_central_atom, include_hydrogens)):
                    if folded[j] == 1:
                        mapping_dict[i].add(s)

        if mapping and atom_index_mapping:
            return fingerprints, mapping_dict, atom_index_mapping_dict
        elif mapping:
            return fingerprints, mapping_dict
        elif atom_index_mapping:
            return fingerprints, atom_index_mapping_dict
        else:
            return fingerprints
