
import numpy as np
from typing import List, Dict, Set, Tuple, Union, Iterable
from rdkit.Chem import Mol
from collections import defaultdict
import hashlib


class DRFPUtil:

    @staticmethod
    def shingling_from_mol(in_mol: Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        from rdkit.Chem import MolToSmiles, GetSymmSSSR, AtomIndices
        from rdkit.Chem.rdmolops import GetAdjacencyMatrix

        shingles = []
        atom_indices_map = defaultdict(list)

        if rings:
            sssr = GetSymmSSSR(in_mol)
            for ring in sssr:
                ring_atoms = set(ring)
                if len(ring_atoms) >= min_radius:
                    smiles = MolToSmiles(in_mol, atomsToUse=list(
                        ring_atoms), rootedAtAtom=-1 if not root_central_atom else min(ring_atoms))
                    shingles.append(smiles)
                    if get_atom_indices:
                        atom_indices_map[smiles].append(ring_atoms)

        for atom in in_mol.GetAtoms():
            if not include_hydrogens and atom.GetAtomicNum() == 1:
                continue
            for r in range(min_radius, radius + 1):
                env = Chem.FindAtomEnvironmentOfRadiusN(
                    in_mol, r, atom.GetIdx())
                atoms_in_env = set()
                for bidx in env:
                    atoms_in_env.add(in_mol.GetBondWithIdx(
                        bidx).GetBeginAtomIdx())
                    atoms_in_env.add(
                        in_mol.GetBondWithIdx(bidx).GetEndAtomIdx())
                if len(atoms_in_env) > 0:
                    smiles = MolToSmiles(in_mol, atomsToUse=list(
                        atoms_in_env), rootedAtAtom=-1 if not root_central_atom else atom.GetIdx())
                    shingles.append(smiles)
                    if get_atom_indices:
                        atom_indices_map[smiles].append(atoms_in_env)

        if get_atom_indices:
            return shingles, atom_indices_map
        return shingles

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        from rdkit.Chem import MolFromSmiles
        mol = MolFromSmiles(in_smiles)
        if mol is None:
            raise ValueError("Invalid SMILES string provided.")

        if get_atom_indices:
            shingles, atom_indices_map = DRFPUtil.shingling_from_mol(
                mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
            hashed = DRFPUtil.hash(shingles)
            folded, folded_indices = DRFPUtil.fold(hashed)
            return folded, folded_indices, {in_smiles: [atom_indices_map]}
        else:
            shingles = DRFPUtil.shingling_from_mol(
                mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
            hashed = DRFPUtil.hash(shingles)
            folded, folded_indices = DRFPUtil.fold(hashed)
            return folded, folded_indices

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        hashes = []
        for shingle in shingling:
            h = int(hashlib.sha256(shingle.encode(
                'utf-8')).hexdigest(), 16) % (10**8)
            hashes.append(h)
        return np.array(hashes, dtype=np.uint32)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        folded = np.zeros(length, dtype=np.uint8)
        folded_indices = np.zeros(length, dtype=np.uint32)
        for h in hash_values:
            idx = h % length
            folded[idx] = 1
            folded_indices[idx] = h
        return folded, folded_indices

    @staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        from tqdm import tqdm

        if isinstance(X, str):
            X = [X]

        fingerprints = []
        feature_mapping = defaultdict(set)
        atom_mappings = []

        iterable = tqdm(X) if show_progress_bar else X

        for i, smiles in enumerate(iterable):
            if atom_index_mapping:
                folded, folded_indices, atom_map = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, True, root_central_atom, include_hydrogens)
                atom_mappings.append(atom_map)
            elif mapping:
                folded, folded_indices = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, False, root_central_atom, include_hydrogens)
            else:
                folded, _ = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, False, root_central_atom, include_hydrogens)

            fingerprints.append(folded)

            if mapping:
                for idx, h in enumerate(folded_indices):
                    if folded[idx] == 1:
                        feature_mapping[idx].add(str(h))

        if mapping and atom_index_mapping:
            return fingerprints, feature_mapping, atom_mappings
        elif mapping:
            return fingerprints, feature_mapping
        elif atom_index_mapping:
            return fingerprints, atom_mappings
        else:
            return fingerprints
