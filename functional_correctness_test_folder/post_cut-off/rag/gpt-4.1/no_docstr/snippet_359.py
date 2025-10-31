
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
        atom_indices_map = defaultdict(list)
        # Optionally add explicit hydrogens
        if include_hydrogens:
            mol = Chem.AddHs(in_mol)
        else:
            mol = in_mol

        n_atoms = mol.GetNumAtoms()
        for atom_idx in range(n_atoms):
            for rad in range(min_radius, radius + 1):
                env = Chem.FindAtomEnvironmentOfRadiusN(mol, rad, atom_idx)
                if not env:
                    continue
                atoms_in_env = set()
                for bidx in env:
                    bond = mol.GetBondWithIdx(bidx)
                    atoms_in_env.add(bond.GetBeginAtomIdx())
                    atoms_in_env.add(bond.GetEndAtomIdx())
                atoms_in_env.add(atom_idx)
                submol = Chem.PathToSubmol(mol, env)
                if root_central_atom:
                    try:
                        smiles = Chem.MolToSmiles(
                            submol, rootedAtAtom=atom_idx, canonical=True)
                    except Exception:
                        smiles = Chem.MolToSmiles(submol, canonical=True)
                else:
                    smiles = Chem.MolToSmiles(submol, canonical=True)
                shingling.append(smiles)
                if get_atom_indices:
                    atom_indices_map[smiles].append(atoms_in_env)
        # Optionally add rings
        if rings:
            sssr = list(GetSymmSSSR(mol))
            for ring in sssr:
                ring_atoms = list(ring)
                bonds = []
                for i in range(len(ring_atoms)):
                    a1 = ring_atoms[i]
                    a2 = ring_atoms[(i + 1) % len(ring_atoms)]
                    bond = mol.GetBondBetweenAtoms(a1, a2)
                    if bond is not None:
                        bonds.append(bond.GetIdx())
                if not bonds:
                    continue
                submol = Chem.PathToSubmol(mol, bonds)
                if root_central_atom:
                    try:
                        smiles = Chem.MolToSmiles(
                            submol, rootedAtAtom=ring_atoms[0], canonical=True)
                    except Exception:
                        smiles = Chem.MolToSmiles(submol, canonical=True)
                else:
                    smiles = Chem.MolToSmiles(submol, canonical=True)
                shingling.append(smiles)
                if get_atom_indices:
                    atom_indices_map[smiles].append(set(ring_atoms))
        if get_atom_indices:
            return shingling, dict(atom_indices_map)
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
        mols = []
        for part in [reactants, products]:
            mols_part = []
            for smi in part.split("."):
                smi = smi.strip()
                if smi:
                    mol = Chem.MolFromSmiles(smi)
                    if mol is not None:
                        mols_part.append(mol)
            mols.append(mols_part)
        reactant_mols, product_mols = mols
        shingling = []
        atom_indices_mapping = {}
        for label, mol_list in zip(['reactants', 'products'], [reactant_mols, product_mols]):
            for mol in mol_list:
                if get_atom_indices:
                    s, idx_map = DRFPUtil.shingling_from_mol(
                        mol, radius=radius, rings=rings, min_radius=min_radius,
                        get_atom_indices=True, root_central_atom=root_central_atom,
                        include_hydrogens=include_hydrogens
                    )
                    shingling.extend(s)
                    for k, v in idx_map.items():
                        if k not in atom_indices_mapping:
                            atom_indices_mapping[k] = []
                        atom_indices_mapping[k].extend(v)
                else:
                    s = DRFPUtil.shingling_from_mol(
                        mol, radius=radius, rings=rings, min_radius=min_radius,
                        get_atom_indices=False, root_central_atom=root_central_atom,
                        include_hydrogens=include_hydrogens
                    )
                    shingling.extend(s)
        # Remove duplicates
        shingling = list(set(shingling))
        hash_values = DRFPUtil.hash(shingling)
        if get_atom_indices:
            return hash_values, np.array(shingling), atom_indices_mapping
        return hash_values, np.array(shingling)

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        '''Directly hash all the SMILES in a shingling to a 32-bit integer.'''
        hashes = []
        for s in shingling:
            # Use a stable hash (md5) and take 32 bits
            h = int(hashlib.md5(s.encode('utf-8')).hexdigest()[:8], 16)
            hashes.append(h)
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
        fingerprints = []
        feature_mapping = defaultdict(set)
        atom_indices_mappings = []
        iterator = X
        if show_progress_bar:
            try:
                from tqdm import tqdm
                iterator = tqdm(X)
            except ImportError:
                pass
        for idx, smiles in enumerate(iterator):
            if atom_index_mapping:
                hash_values, shingling, atom_indices_map = DRFPUtil.internal_encode(
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
            folded, on_bits = DRFPUtil.fold(
                hash_values, length=n_folded_length)
            fingerprints.append(folded)
            if mapping:
                for i in on_bits:
                    feature_mapping[i].update(
                        shingling[np.mod(hash_values, n_folded_length) == i])
            if atom_index_mapping:
                atom_indices_mappings.append(atom_indices_map)
        if mapping and atom_index_mapping:
            return fingerprints, dict(feature_mapping), atom_indices_mappings
        elif mapping:
            return fingerprints, dict(feature_mapping)
        elif atom_index_mapping:
            return fingerprints, atom_indices_mappings
        else:
            return fingerprints
