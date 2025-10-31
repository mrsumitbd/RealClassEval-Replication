
import numpy as np
from typing import List, Tuple, Dict, Set, Union, Iterable
from rdkit import Chem
from rdkit.Chem.rdchem import Mol
from tqdm import tqdm


class DRFPUtil:
    '''
    A utility class for encoding SMILES as drfp fingerprints.
    '''

    @staticmethod
    def shingling_from_mol(in_mol: Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        '''Creates a molecular shingling from a RDKit molecule (rdkit.Chem.rdchem.Mol).'''
        from rdkit.Chem import rdmolops

        if in_mol is None:
            return [] if not get_atom_indices else ([], {})

        if include_hydrogens:
            in_mol = Chem.AddHs(in_mol)

        shingling = []
        atom_indices = {}

        for atom in in_mol.GetAtoms():
            for r in range(min_radius, radius + 1):
                env = rdmolops.FindAtomEnvironmentOfRadiusN(
                    in_mol, r, atom.GetIdx())
                if not env:
                    continue

                amap = {}
                submol = rdmolops.PathToSubmol(in_mol, env, atomMap=amap)

                if submol is None:
                    continue

                if root_central_atom:
                    smiles = Chem.MolToSmiles(
                        submol, rootedAtAtom=amap[atom.GetIdx()], canonical=True)
                else:
                    smiles = Chem.MolToSmiles(submol, canonical=True)

                shingling.append(smiles)

                if get_atom_indices:
                    if smiles not in atom_indices:
                        atom_indices[smiles] = []
                    atom_indices[smiles].append(set(amap.values()))

        if rings:
            sssr = Chem.GetSymmSSSR(in_mol)
            for ring in sssr:
                ri = list(ring)
                env = set()
                for i in range(len(ri)):
                    for j in range(i + 1, len(ri)):
                        bond = in_mol.GetBondBetweenAtoms(ri[i], ri[j])
                        if bond:
                            env.add(bond.GetIdx())

                amap = {}
                submol = rdmolops.PathToSubmol(in_mol, list(env), atomMap=amap)

                if submol is None:
                    continue

                smiles = Chem.MolToSmiles(submol, canonical=True)
                shingling.append(smiles)

                if get_atom_indices:
                    if smiles not in atom_indices:
                        atom_indices[smiles] = []
                    atom_indices[smiles].append(set(amap.values()))

        if get_atom_indices:
            return (shingling, atom_indices)
        return shingling

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        '''Creates an drfp array from a reaction SMILES string.'''
        from rdkit.Chem import AllChem

        reactants, products = in_smiles.split('>>')
        r_mol = AllChem.MolFromSmiles(reactants)
        p_mol = AllChem.MolFromSmiles(products)

        r_shingling = DRFPUtil.shingling_from_mol(
            r_mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)
        p_shingling = DRFPUtil.shingling_from_mol(
            p_mol, radius, rings, min_radius, get_atom_indices, root_central_atom, include_hydrogens)

        if get_atom_indices:
            r_shingles, r_atom_indices = r_shingling
            p_shingles, p_atom_indices = p_shingling
            shingling = r_shingles + ['>>'] + p_shingles
            atom_indices = {'reactants': r_atom_indices,
                            'products': p_atom_indices}
        else:
            shingling = r_shingling + ['>>'] + p_shingling
            atom_indices = {}

        hashed = DRFPUtil.hash(shingling)

        if get_atom_indices:
            return (hashed, np.array(shingling), atom_indices)
        return (hashed, np.array(shingling))

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        '''Directly hash all the SMILES in a shingling to a 32-bit integer.'''
        import mmh3
        return np.array([mmh3.hash(s, signed=False) for s in shingling], dtype=np.uint32)

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        '''Folds the hash values to a binary vector of a given length.'''
        indices = hash_values % length
        fingerprint = np.zeros(length, dtype=np.uint8)
        np.add.at(fingerprint, indices, 1)
        fingerprint = np.clip(fingerprint, 0, 1)
        return (fingerprint, indices)

    @staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        '''Encodes a list of reaction SMILES using the drfp fingerprint.'''
        if isinstance(X, str):
            X = [X]

        fingerprints = []
        mappings = {}
        atom_mappings = []

        iterator = tqdm(X) if show_progress_bar else X

        for i, smiles in enumerate(iterator):
            if atom_index_mapping:
                hashed, shingling, atom_indices = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, True, root_central_atom, include_hydrogens)
                atom_mappings.append(atom_indices)
            elif mapping:
                hashed, shingling = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, False, root_central_atom, include_hydrogens)
            else:
                hashed, _ = DRFPUtil.internal_encode(
                    smiles, radius, min_radius, rings, False, root_central_atom, include_hydrogens)

            fingerprint, _ = DRFPUtil.fold(hashed, n_folded_length)
            fingerprints.append(fingerprint)

            if mapping:
                for h, s in zip(hashed, shingling):
                    h_mod = h % n_folded_length
                    if h_mod not in mappings:
                        mappings[h_mod] = set()
                    mappings[h_mod].add(s)

        if atom_index_mapping:
            return (fingerprints, mappings, atom_mappings) if mapping else (fingerprints, atom_mappings)
        return (fingerprints, mappings) if mapping else fingerprints
