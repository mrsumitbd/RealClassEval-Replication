
from typing import List, Tuple, Dict, Set, Union, Iterable
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdmolops
from rdkit.Chem.rdmolops import GetShortestPath
from rdkit.Chem.rdchem import Mol
from collections import defaultdict
import hashlib


class DRFPUtil:
    '''
    A utility class for encoding SMILES as drfp fingerprints.
    '''
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
        if not include_hydrogens:
            in_mol = Chem.RemoveHs(in_mol)
        n_atoms = in_mol.GetNumAtoms()
        shingling = set()
        shingling_indices = defaultdict(list)
        for atom_idx in range(n_atoms):
            for r in range(min_radius, radius + 1):
                env = Chem.FindAtomEnvironmentOfRadiusN(in_mol, r, atom_idx)
                if not env:
                    continue
                atoms = set()
                for bidx in env:
                    bond = in_mol.GetBondWithIdx(bidx)
                    atoms.add(bond.GetBeginAtomIdx())
                    atoms.add(bond.GetEndAtomIdx())
                atoms.add(atom_idx)
                submol = Chem.PathToSubmol(
                    in_mol, env, atomMap={i: i for i in atoms})
                if root_central_atom:
                    smiles = Chem.MolToSmiles(
                        submol, rootedAtAtom=atom_idx, canonical=True)
                else:
                    smiles = Chem.MolToSmiles(submol, canonical=True)
                shingling.add(smiles)
                if get_atom_indices:
                    shingling_indices[smiles].append(set(atoms))
        # Add rings if requested
        if rings:
            ssr = rdmolops.GetSymmSSSR(in_mol)
            for ring in ssr:
                ring_atoms = list(ring)
                ring_bonds = []
                for i in range(len(ring_atoms)):
                    a1 = ring_atoms[i]
                    a2 = ring_atoms[(i + 1) % len(ring_atoms)]
                    bond = in_mol.GetBondBetweenAtoms(a1, a2)
                    if bond is not None:
                        ring_bonds.append(bond.GetIdx())
                submol = Chem.PathToSubmol(in_mol, ring_bonds, atomMap={
                                           i: i for i in ring_atoms})
                if root_central_atom:
                    smiles = Chem.MolToSmiles(
                        submol, rootedAtAtom=ring_atoms[0], canonical=True)
                else:
                    smiles = Chem.MolToSmiles(submol, canonical=True)
                shingling.add(smiles)
                if get_atom_indices:
                    shingling_indices[smiles].append(set(ring_atoms))
        if get_atom_indices:
            return list(shingling), dict(shingling_indices)
        else:
            return list(shingling)

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
        parts = in_smiles.split(">")
        if len(parts) == 3:
            reactants, agents, products = parts
        elif len(parts) == 1:
            reactants, products = parts[0].split(">>")
            agents = ""
        else:
            raise ValueError("Invalid reaction SMILES: %s" % in_smiles)
        mols = []
        for part in [reactants, products]:
            for smi in part.split("."):
                smi = smi.strip()
                if smi:
                    mol = Chem.MolFromSmiles(smi)
                    if mol is not None:
                        mols.append(mol)
        shingling = []
        shingling_indices = {}
        if get_atom_indices:
            for mol in mols:
                s, idx = DRFPUtil.shingling_from_mol(
                    mol, radius=radius, rings=rings, min_radius=min_radius,
                    get_atom_indices=True, root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                shingling.extend(s)
                for k, v in idx.items():
                    if k not in shingling_indices:
                        shingling_indices[k] = []
                    shingling_indices[k].extend(v)
        else:
            for mol in mols:
                s = DRFPUtil.shingling_from_mol(
                    mol, radius=radius, rings=rings, min_radius=min_radius,
                    get_atom_indices=False, root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                shingling.extend(s)
        shingling = list(set(shingling))
        hash_values = DRFPUtil.hash(shingling)
        if get_atom_indices:
            return hash_values, np.array(shingling), shingling_indices
        else:
            return hash_values, np.array(shingling)

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        hashes = []
        for s in shingling:
            # Use a stable hash (md5) and take 4 bytes as int32
            h = hashlib.md5(s.encode("utf-8")).digest()
            val = int.from_bytes(h[:4], byteorder="little", signed=False)
            hashes.append(val)
        return np.array(hashes, dtype=np.uint32)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        folded = np.zeros(length, dtype=np.uint8)
        on_bits = np.mod(hash_values, length)
        folded[on_bits] = 1
        return folded, on_bits

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
        mapping_dict = defaultdict(set)
        atom_index_dict = []
        for idx, smiles in enumerate(iterator):
            if atom_index_mapping:
                hash_values, shingling, shingling_indices = DRFPUtil.internal_encode(
                    smiles, radius=radius, min_radius=min_radius, rings=rings,
                    get_atom_indices=True, root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
            else:
                hash_values, shingling = DRFPUtil.internal_encode(
                    smiles, radius=radius, min_radius=min_radius, rings=rings,
                    get_atom_indices=False, root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
            folded, on_bits = DRFPUtil.fold(hash_values, n_folded_length)
            fps.append(folded)
            if mapping or atom_index_mapping:
                for i, bit in enumerate(on_bits):
                    mapping_dict[bit].add(shingling[i])
            if atom_index_mapping:
                atom_index_dict.append(shingling_indices)
        if mapping or atom_index_mapping:
            if atom_index_mapping:
                return fps, dict(mapping_dict), atom_index_dict
            else:
                return fps, dict(mapping_dict)
        else:
            return fps
