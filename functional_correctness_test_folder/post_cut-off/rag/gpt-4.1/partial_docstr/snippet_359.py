
import numpy as np
from typing import List, Tuple, Dict, Set, Union, Iterable
from rdkit import Chem
from rdkit.Chem import rdmolops
from rdkit.Chem.rdmolops import GetShortestPath
from rdkit.Chem.rdmolops import GetSymmSSSR
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
        '''Creates a molecular shingling from a RDKit molecule (rdkit.Chem.rdchem.Mol).'''
        if in_mol is None:
            if get_atom_indices:
                return [], {}
            return []
        shingling = []
        atom_index_map = defaultdict(list)
        n_atoms = in_mol.GetNumAtoms()
        for atom_idx in range(n_atoms):
            for rad in range(min_radius, radius + 1):
                env = Chem.FindAtomEnvironmentOfRadiusN(in_mol, rad, atom_idx)
                if not env:
                    continue
                atoms_in_env = set()
                for bidx in env:
                    bond = in_mol.GetBondWithIdx(bidx)
                    atoms_in_env.add(bond.GetBeginAtomIdx())
                    atoms_in_env.add(bond.GetEndAtomIdx())
                atoms_in_env.add(atom_idx)
                submol = Chem.PathToSubmol(
                    in_mol, env, includeHydrogens=include_hydrogens)
                if root_central_atom:
                    try:
                        amap = {}
                        smi = Chem.MolToSmiles(
                            submol, rootedAtAtom=atom_idx, canonical=True, isomericSmiles=True, atomMap=amap)
                    except Exception:
                        smi = Chem.MolToSmiles(
                            submol, canonical=True, isomericSmiles=True)
                else:
                    smi = Chem.MolToSmiles(
                        submol, canonical=True, isomericSmiles=True)
                shingling.append(smi)
                if get_atom_indices:
                    atom_index_map[smi].append(atoms_in_env)
        if rings:
            sssr = list(GetSymmSSSR(in_mol))
            for ring in sssr:
                ring_atoms = set(ring)
                bonds = []
                for i, a1 in enumerate(ring):
                    a2 = ring[(i + 1) % len(ring)]
                    bond = in_mol.GetBondBetweenAtoms(int(a1), int(a2))
                    if bond is not None:
                        bonds.append(bond.GetIdx())
                if bonds:
                    submol = Chem.PathToSubmol(
                        in_mol, bonds, includeHydrogens=include_hydrogens)
                    smi = Chem.MolToSmiles(
                        submol, canonical=True, isomericSmiles=True)
                    shingling.append(smi)
                    if get_atom_indices:
                        atom_index_map[smi].append(ring_atoms)
        if get_atom_indices:
            return shingling, dict(atom_index_map)
        return shingling

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
        '''Creates an drfp array from a reaction SMILES string.'''
        # Split reaction SMILES into reactants, agents, products
        if ">" in in_smiles:
            parts = in_smiles.split(">")
            if len(parts) == 3:
                reactants, agents, products = parts
            elif len(parts) == 2:
                reactants, products = parts
                agents = ""
            else:
                reactants = in_smiles
                agents = ""
                products = ""
        else:
            reactants = in_smiles
            agents = ""
            products = ""
        mols = []
        for part in [reactants, products]:
            for smi in part.split("."):
                smi = smi.strip()
                if smi:
                    mol = Chem.MolFromSmiles(smi)
                    if mol is not None:
                        mols.append(mol)
        shinglings = []
        atom_index_maps = []
        for mol in mols:
            if get_atom_indices:
                shing, atom_map = DRFPUtil.shingling_from_mol(
                    mol, radius=radius, rings=rings, min_radius=min_radius,
                    get_atom_indices=True, root_central_atom=root_central_atom, include_hydrogens=include_hydrogens
                )
                shinglings.extend(shing)
                atom_index_maps.append(atom_map)
            else:
                shing = DRFPUtil.shingling_from_mol(
                    mol, radius=radius, rings=rings, min_radius=min_radius,
                    get_atom_indices=False, root_central_atom=root_central_atom, include_hydrogens=include_hydrogens
                )
                shinglings.extend(shing)
        hash_values = DRFPUtil.hash(shinglings)
        shinglings_arr = np.array(shinglings, dtype=object)
        if get_atom_indices:
            return hash_values, shinglings_arr, atom_index_maps
        return hash_values, shinglings_arr

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        '''Directly hash all the SMILES in a shingling to a 32-bit integer.'''
        hashes = []
        for s in shingling:
            # Use a stable hash (md5) and take 4 bytes as int32
            h = hashlib.md5(s.encode("utf-8")).digest()
            val = int.from_bytes(h[:4], "little", signed=False)
            hashes.append(val)
        return np.array(hashes, dtype=np.uint32)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        '''Folds the hash values to a binary vector of a given length.'''
        folded = np.zeros(length, dtype=np.uint8)
        indices = np.mod(hash_values, length)
        folded[indices] = 1
        on_bits = np.where(folded == 1)[0]
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
        '''Encodes a list of reaction SMILES using the drfp fingerprint.'''
        if isinstance(X, str):
            X = [X]
        else:
            X = list(X)
        results = []
        mapping_dict = defaultdict(set)
        atom_index_maps = []
        if show_progress_bar:
            try:
                from tqdm import tqdm
                iterator = tqdm(X)
            except ImportError:
                iterator = X
        else:
            iterator = X
        for idx, smiles in enumerate(iterator):
            if atom_index_mapping:
                hash_vals, shing_arr, atom_maps = DRFPUtil.internal_encode(
                    smiles, radius=radius, min_radius=min_radius, rings=rings,
                    get_atom_indices=True, root_central_atom=root_central_atom, include_hydrogens=include_hydrogens
                )
                atom_index_maps.append(atom_maps)
            else:
                hash_vals, shing_arr = DRFPUtil.internal_encode(
                    smiles, radius=radius, min_radius=min_radius, rings=rings,
                    get_atom_indices=False, root_central_atom=root_central_atom, include_hydrogens=include_hydrogens
                )
            folded, on_bits = DRFPUtil.fold(hash_vals, length=n_folded_length)
            results.append(folded)
            if mapping:
                for i in on_bits:
                    mapping_dict[i].update(
                        shing_arr[np.mod(hash_vals, n_folded_length) == i])
        if atom_index_mapping:
            return atom_index_maps
        if mapping:
            return results, dict(mapping_dict)
        return results
