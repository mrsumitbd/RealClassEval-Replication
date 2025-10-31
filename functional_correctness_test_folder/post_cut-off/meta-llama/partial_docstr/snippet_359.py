
from typing import List, Tuple, Union, Iterable, Dict, Set
from rdkit import Chem
from rdkit.Chem import Mol
import numpy as np
from tqdm import tqdm


class DRFPUtil:

    @staticmethod
    def shingling_from_mol(in_mol: Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        shingling = []
        atom_indices = {}
        for atom in in_mol.GetAtoms():
            if not include_hydrogens and atom.GetAtomicNum() == 1:
                continue
            for r in range(min_radius, radius + 1):
                if r == 0:
                    smiles = Chem.MolFragmentToSmiles(
                        in_mol, [atom.GetIdx()], rootedAtAtom=root_central_atom)
                    shingling.append(smiles)
                    if get_atom_indices:
                        if smiles not in atom_indices:
                            atom_indices[smiles] = []
                        atom_indices[smiles].append({atom.GetIdx()})
                else:
                    env = Chem.FindAtomEnvironmentOfRadiusN(
                        in_mol, r, atom.GetIdx())
                    if env:
                        atoms_to_use = set()
                        for bidx in env:
                            atoms_to_use.add(in_mol.GetBondWithIdx(
                                bidx).GetBeginAtomIdx())
                            atoms_to_use.add(
                                in_mol.GetBondWithIdx(bidx).GetEndAtomIdx())
                        if not include_hydrogens:
                            atoms_to_use = {a for a in atoms_to_use if in_mol.GetAtomWithIdx(
                                a).GetAtomicNum() != 1}
                        if len(atoms_to_use) > 0:
                            smiles = Chem.MolFragmentToSmiles(
                                in_mol, atoms_to_use, rootedAtAtom=root_central_atom)
                            shingling.append(smiles)
                            if get_atom_indices:
                                if smiles not in atom_indices:
                                    atom_indices[smiles] = []
                                atom_indices[smiles].append(atoms_to_use)
        if rings:
            for ring in in_mol.GetRingInfo().AtomRings():
                if not include_hydrogens:
                    ring = {a for a in ring if in_mol.GetAtomWithIdx(
                        a).GetAtomicNum() != 1}
                if len(ring) > 0:
                    smiles = Chem.MolFragmentToSmiles(
                        in_mol, ring, rootedAtAtom=root_central_atom)
                    shingling.append(smiles)
                    if get_atom_indices:
                        if smiles not in atom_indices:
                            atom_indices[smiles] = []
                        atom_indices[smiles].append(ring)
        if get_atom_indices:
            return shingling, atom_indices
        else:
            return shingling

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        mol = Chem.MolFromSmiles(in_smiles)
        if mol is None:
            return np.array([]), np.array([])
        shingling, atom_indices = DRFPUtil.shingling_from_mol(
            mol, radius=radius, min_radius=min_radius, rings=rings, get_atom_indices=True, root_central_atom=root_central_atom, include_hydrogens=include_hydrogens)
        hash_values = DRFPUtil.hash(shingling)
        if get_atom_indices:
            return hash_values, np.ones_like(hash_values), {in_smiles: [atom_indices]}
        else:
            return hash_values, np.ones_like(hash_values)

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        return np.array([hash(s) % (2**32) for s in shingling], dtype=np.uint32)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        folded = hash_values % length
        counts = np.bincount(folded, minlength=length)
        return np.where(counts > 0)[0].astype(np.uint32), counts[counts > 0].astype(np.uint32)

    @staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        if isinstance(X, str):
            X = [X]
        fingerprints = []
        mappings = []
        for x in tqdm(X, desc="Encoding reactions", disable=not show_progress_bar):
            try:
                reactants, products = x.split(">>")
                reactant_hash_values, reactant_counts, reactant_atom_indices = DRFPUtil.internal_encode(
                    reactants, radius=radius, min_radius=min_radius, rings=rings, get_atom_indices=atom_index_mapping, root_central_atom=root_central_atom, include_hydrogens=include_hydrogens)
                product_hash_values, product_counts, product_atom_indices = DRFPUtil.internal_encode(
                    products, radius=radius, min_radius=min_radius, rings=rings, get_atom_indices=atom_index_mapping, root_central_atom=root_central_atom, include_hydrogens=include_hydrogens)
                hash_values = np.concatenate(
                    [reactant_hash_values, -product_hash_values])
                counts = np.concatenate([reactant_counts, product_counts])
                folded, counts = DRFPUtil.fold(
                    hash_values, length=n_folded_length)
                fingerprints.append(counts)
                if mapping or atom_index_mapping:
                    atom_indices = {}
                    for smiles, indices in {**reactant_atom_indices, **product_atom_indices}.items():
                        for index in indices:
                            for idx in index:
                                if idx not in atom_indices:
                                    atom_indices[idx] = set()
                                atom_indices[idx].add(smiles)
                    if mapping:
                        mappings.append({k: list(v)
                                        for k, v in atom_indices.items()})
                    if atom_index_mapping:
                        mappings.append(
                            {**reactant_atom_indices, **product_atom_indices})
            except Exception as e:
                fingerprints.append(np.array([]))
                mappings.append({})
        if mapping or atom_index_mapping:
            return fingerprints, mappings
        else:
            return fingerprints
