
import numpy as np
from typing import Union, List, Tuple, Dict, Set, Iterable
from rdkit import Chem
from rdkit.Chem import rdChemReactions
from collections import defaultdict
import hashlib
from tqdm import tqdm


class DRFPUtil:
    '''
    A utility class for encoding SMILES as drfp fingerprints.
    '''
    @staticmethod
    def shingling_from_mol(in_mol: Chem.Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        '''Creates a molecular shingling from a RDKit molecule (rdkit.Chem.rdchem.Mol).'''
        shingling = []
        atom_indices_dict = defaultdict(list)

        if include_hydrogens:
            in_mol = Chem.AddHs(in_mol)

        for atom in in_mol.GetAtoms():
            if not include_hydrogens and atom.GetAtomicNum() == 1:
                continue

            for r in range(min_radius, radius + 1):
                env = Chem.FindAtomEnvironmentOfRadiusN(
                    in_mol, r, atom.GetIdx())
                if not env:
                    continue

                amap = {}
                submol = Chem.PathToSubmol(in_mol, env, atomMap=amap)
                if not submol:
                    continue

                if root_central_atom:
                    smiles = Chem.MolToSmiles(
                        submol, rootedAtAtom=amap[atom.GetIdx()], canonical=True)
                else:
                    smiles = Chem.MolToSmiles(submol, canonical=True)

                shingling.append(smiles)

                if get_atom_indices:
                    atom_indices = set(amap.keys())
                    atom_indices_dict[smiles].append(atom_indices)

        if rings:
            for ring in Chem.GetSymmSSSR(in_mol):
                ring_atoms = list(ring)
                if len(ring_atoms) < 3:
                    continue

                bond_ids = []
                for i in range(len(ring_atoms)):
                    for j in range(i + 1, len(ring_atoms)):
                        bond = in_mol.GetBondBetweenAtoms(
                            ring_atoms[i], ring_atoms[j])
                        if bond:
                            bond_ids.append(bond.GetIdx())

                if not bond_ids:
                    continue

                amap = {}
                submol = Chem.PathToSubmol(in_mol, bond_ids, atomMap=amap)
                if not submol:
                    continue

                smiles = Chem.MolToSmiles(submol, canonical=True)
                shingling.append(smiles)

                if get_atom_indices:
                    atom_indices = set(amap.keys())
                    atom_indices_dict[smiles].append(atom_indices)

        if get_atom_indices:
            return shingling, atom_indices_dict
        return shingling

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        '''Creates an drfp array from a reaction SMILES string.'''
        rxn = rdChemReactions.ReactionFromSmarts(in_smiles, useSmiles=True)
        reactants = rxn.GetReactants()
        products = rxn.GetProducts()

        all_shingles = []
        atom_indices_mapping = defaultdict(list)

        for mol in reactants + products:
            if get_atom_indices:
                shingles, atom_indices = DRFPUtil.shingling_from_mol(
                    mol, radius, rings, min_radius, True, root_central_atom, include_hydrogens
                )
                for smiles, indices in atom_indices.items():
                    atom_indices_mapping[smiles].append({'reactants': indices})
            else:
                shingles = DRFPUtil.shingling_from_mol(
                    mol, radius, rings, min_radius, False, root_central_atom, include_hydrogens
                )
            all_shingles.extend(shingles)

        unique_shingles = list(set(all_shingles))
        hashed_shingles = DRFPUtil.hash(unique_shingles)

        if get_atom_indices:
            return hashed_shingles, np.array(unique_shingles), atom_indices_mapping
        return hashed_shingles, np.array(unique_shingles)

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        '''Directly hash all the SMILES in a shingling to a 32-bit integer.'''
        hashed = []
        for s in shingling:
            h = int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % (2**32)
            hashed.append(h)
        return np.array(hashed, dtype=np.uint32)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        '''Folds the hash values to a binary vector of a given length.'''
        folded = np.zeros(length, dtype=np.uint8)
        indices = np.unique(hash_values % length)
        folded[indices] = 1
        return folded, indices

    @staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        '''Encodes a list of reaction SMILES using the drfp fingerprint.'''
        if isinstance(X, str):
            X = [X]

        fingerprints = []
        feature_mapping = {}
        atom_mappings = []

        iterable = tqdm(X) if show_progress_bar else X

        for i, smiles in enumerate(iterable):
            if atom_index_mapping:
                hashed, shingles, atom_indices = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, True, root_central_atom, include_hydrogens
                )
                atom_mappings.append(atom_indices)
            elif mapping:
                hashed, shingles = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, False, root_central_atom, include_hydrogens
                )
            else:
                hashed, _ = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, False, root_central_atom, include_hydrogens
                )

            folded, indices = DRFPUtil.fold(hashed, n_folded_length)
            fingerprints.append(folded)

            if mapping:
                for idx in indices:
                    if idx not in feature_mapping:
                        feature_mapping[idx] = set()
                    feature_mapping[idx].add(
                        shingles[np.where(hashed % n_folded_length == idx)[0][0]])

        if atom_index_mapping:
            if mapping:
                return fingerprints, feature_mapping, atom_mappings
            return fingerprints, atom_mappings
        elif mapping:
            return fingerprints, feature_mapping
        return fingerprints
