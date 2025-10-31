
from typing import List, Tuple, Dict, Set, Union, Iterable
import numpy as np

from rdkit import Chem
from rdkit.Chem import rdmolops
from rdkit.Chem.rdchem import Mol
from collections import defaultdict
import hashlib


class DRFPUtil:

    @staticmethod
    def shingling_from_mol(
        in_mol: Mol,
        radius: int = 3,
        rings: bool = True,
        min_radius: int = 0,
        get_atom_indices: bool = False,
        root_central_atom: bool = True,
        include_hydrogens: bool = False
    ) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        if in_mol is None:
            if get_atom_indices:
                return [], {}
            else:
                return []
        mol = Chem.RWMol(in_mol)
        if include_hydrogens:
            mol = Chem.AddHs(mol)
        n_atoms = mol.GetNumAtoms()
        shinglings = []
        shingling_atom_indices = defaultdict(list)
        # Spheres
        for atom_idx in range(n_atoms):
            for r in range(min_radius, radius + 1):
                env = Chem.FindAtomEnvironmentOfRadiusN(mol, r, atom_idx)
                if not env:
                    continue
                atoms = set()
                for bidx in env:
                    bond = mol.GetBondWithIdx(bidx)
                    atoms.add(bond.GetBeginAtomIdx())
                    atoms.add(bond.GetEndAtomIdx())
                atoms.add(atom_idx)
                submol = Chem.PathToSubmol(mol, env)
                if root_central_atom:
                    try:
                        smiles = Chem.MolToSmiles(
                            submol, rootedAtAtom=atom_idx, canonical=True)
                    except Exception:
                        smiles = Chem.MolToSmiles(submol, canonical=True)
                else:
                    smiles = Chem.MolToSmiles(submol, canonical=True)
                shinglings.append(smiles)
                if get_atom_indices:
                    shingling_atom_indices[smiles].append(atoms)
        # Rings
        if rings:
            ri = mol.GetRingInfo()
            for ring_atoms in ri.AtomRings():
                submol = Chem.PathToSubmol(
                    mol, rdmolops.FindBondRing(mol, ring_atoms))
                if root_central_atom and len(ring_atoms) > 0:
                    try:
                        smiles = Chem.MolToSmiles(
                            submol, rootedAtAtom=ring_atoms[0], canonical=True)
                    except Exception:
                        smiles = Chem.MolToSmiles(submol, canonical=True)
                else:
                    smiles = Chem.MolToSmiles(submol, canonical=True)
                shinglings.append(smiles)
                if get_atom_indices:
                    shingling_atom_indices[smiles].append(set(ring_atoms))
        if get_atom_indices:
            return shinglings, dict(shingling_atom_indices)
        else:
            return shinglings

    @staticmethod
    def internal_encode(
        in_smiles: str,
        radius: int = 3,
        min_radius: int = 0,
        rings: bool = True,
        get_atom_indices: bool = False,
        root_central_atom: bool = True,
        include_hydrogens: bool = False
    ) -> Union[
        Tuple[np.ndarray, np.ndarray],
        Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]
    ]:
        # Split reaction SMILES into reactants, agents, products
        if ">>" in in_smiles:
            reactants, products = in_smiles.split(">>")
        else:
            reactants, products = in_smiles, ""
        reactants = reactants.strip()
        products = products.strip()
        reactant_smiles = [s for s in reactants.split(".") if s]
        product_smiles = [s for s in products.split(".") if s]
        reactant_shinglings = []
        product_shinglings = []
        reactant_indices = []
        product_indices = []
        for smi in reactant_smiles:
            mol = Chem.MolFromSmiles(smi)
            if get_atom_indices:
                shinglings, indices = DRFPUtil.shingling_from_mol(
                    mol, radius, rings, min_radius, True, root_central_atom, include_hydrogens
                )
                reactant_shinglings.extend(shinglings)
                reactant_indices.append(indices)
            else:
                shinglings = DRFPUtil.shingling_from_mol(
                    mol, radius, rings, min_radius, False, root_central_atom, include_hydrogens
                )
                reactant_shinglings.extend(shinglings)
        for smi in product_smiles:
            mol = Chem.MolFromSmiles(smi)
            if get_atom_indices:
                shinglings, indices = DRFPUtil.shingling_from_mol(
                    mol, radius, rings, min_radius, True, root_central_atom, include_hydrogens
                )
                product_shinglings.extend(shinglings)
                product_indices.append(indices)
            else:
                shinglings = DRFPUtil.shingling_from_mol(
                    mol, radius, rings, min_radius, False, root_central_atom, include_hydrogens
                )
                product_shinglings.extend(shinglings)
        # Symmetric difference
        reactant_set = set(reactant_shinglings)
        product_set = set(product_shinglings)
        diff = list(reactant_set.symmetric_difference(product_set))
        hash_values = DRFPUtil.hash(diff)
        if get_atom_indices:
            mapping = {
                "reactants": reactant_indices,
                "products": product_indices,
            }
            return hash_values, np.array(diff), mapping
        else:
            return hash_values, np.array(diff)

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        # Use SHA1 hash, convert to int, mod 2**32
        hashes = []
        for s in shingling:
            h = hashlib.sha1(s.encode("utf-8")).hexdigest()
            hashes.append(int(h[:8], 16))
        return np.array(hashes, dtype=np.uint32)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        folded = np.zeros(length, dtype=np.uint8)
        indices = hash_values % length
        for idx in indices:
            folded[idx] = 1
        return folded, indices

    @staticmethod
    def encode(
        X: Union[Iterable, str],
        n_folded_length: int = 2048,
        min_radius: int = 0,
        radius: int = 3,
        rings: bool = True,
        mapping: bool = False,
        atom_index_mapping: bool = False,
        root_central_atom: bool = True,
        include_hydrogens: bool = False,
        show_progress_bar: bool = False
    ) -> Union[
        List[np.ndarray],
        Tuple[List[np.ndarray], Dict[int, Set[str]]],
        Tuple[List[np.ndarray], Dict[int, Set[str]]],
        List[Dict[str, List[Dict[str, List[Set[int]]]]]]
    ]:
        if isinstance(X, str):
            X = [X]
        if show_progress_bar:
            try:
                from tqdm import tqdm
                iterator = tqdm(X)
            except ImportError:
                iterator = X
        else:
            iterator = X
        fps = []
        feature_mapping = defaultdict(set)
        atom_index_mappings = []
        for i, smiles in enumerate(iterator):
            if atom_index_mapping:
                hash_values, diff, mapping_dict = DRFPUtil.internal_encode(
                    smiles,
                    radius=radius,
                    min_radius=min_radius,
                    rings=rings,
                    get_atom_indices=True,
                    root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                fp, indices = DRFPUtil.fold(hash_values, n_folded_length)
                fps.append(fp)
                atom_index_mappings.append(mapping_dict)
                for idx, s in zip(indices, diff):
                    feature_mapping[idx].add(s)
            else:
                hash_values, diff = DRFPUtil.internal_encode(
                    smiles,
                    radius=radius,
                    min_radius=min_radius,
                    rings=rings,
                    get_atom_indices=False,
                    root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                fp, indices = DRFPUtil.fold(hash_values, n_folded_length)
                fps.append(fp)
                for idx, s in zip(indices, diff):
                    feature_mapping[idx].add(s)
        if atom_index_mapping:
            return fps, atom_index_mappings
        elif mapping:
            return fps, dict(feature_mapping)
        else:
            return fps
