import numpy as np
from typing import Any, Dict, Iterable, List, Set, Tuple, Union
from rdkit import Chem
from rdkit.Chem.rdchem import Mol
import hashlib


class DRFPUtil:
    '''
    A utility class for encoding SMILES as drfp fingerprints.
        '''
    @staticmethod
    def shingling_from_mol(in_mol: Mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        '''Creates a molecular shingling from a RDKit molecule (rdkit.Chem.rdchem.Mol).
        Arguments:
            in_mol: A RDKit molecule instance
            radius: The drfp radius (a radius of 3 corresponds to drfp6)
            rings: Whether or not to include rings in the shingling
            min_radius: The minimum radius that is used to extract n-grams
        Returns:
            The molecular shingling.
        '''
        if in_mol is None:
            return ([], {}) if get_atom_indices else []

        mol = Chem.AddHs(in_mol) if include_hydrogens else in_mol

        tokens_set: Set[str] = set()
        atom_map: Dict[str, List[Set[int]]] = {}

        min_r = max(0, int(min_radius))
        max_r = max(min_r, int(radius))

        def _add_token(tok: str, idx_set: Set[int]) -> None:
            tokens_set.add(tok)
            if get_atom_indices:
                atom_map.setdefault(tok, []).append(set(idx_set))

        for a in mol.GetAtoms():
            ai = a.GetIdx()
            for r in range(min_r, max_r + 1):
                if r == 0:
                    atoms_to_use = [ai]
                    bonds_to_use: Tuple[int, ...] = tuple()
                    tok = Chem.MolFragmentToSmiles(
                        mol,
                        atomsToUse=atoms_to_use,
                        bondsToUse=bonds_to_use if bonds_to_use else None,
                        rootedAtAtom=(ai if root_central_atom else -1),
                        canonical=True,
                        isomericSmiles=True,
                    )
                    _add_token(tok, {ai})
                    continue

                env = Chem.FindAtomEnvironmentOfRadiusN(mol, r, ai)
                if not env:
                    continue
                atoms_in_env: Set[int] = set()
                for bid in env:
                    b = mol.GetBondWithIdx(bid)
                    atoms_in_env.add(b.GetBeginAtomIdx())
                    atoms_in_env.add(b.GetEndAtomIdx())
                atoms_to_use = sorted(list(atoms_in_env))
                tok = Chem.MolFragmentToSmiles(
                    mol,
                    atomsToUse=atoms_to_use,
                    bondsToUse=env,
                    rootedAtAtom=(ai if root_central_atom else -1),
                    canonical=True,
                    isomericSmiles=True,
                )
                _add_token(tok, atoms_in_env)

        if rings:
            ring_info = mol.GetRingInfo()
            for ring_bonds in ring_info.BondRings():
                if not ring_bonds:
                    continue
                ring_atoms: Set[int] = set()
                for bid in ring_bonds:
                    b = mol.GetBondWithIdx(bid)
                    ring_atoms.add(b.GetBeginAtomIdx())
                    ring_atoms.add(b.GetEndAtomIdx())
                atoms_to_use = sorted(list(ring_atoms))
                tok = Chem.MolFragmentToSmiles(
                    mol,
                    atomsToUse=atoms_to_use,
                    bondsToUse=ring_bonds,
                    rootedAtAtom=(
                        -1 if not root_central_atom else atoms_to_use[0]),
                    canonical=True,
                    isomericSmiles=True,
                )
                _add_token(tok, ring_atoms)

        tokens = sorted(tokens_set)
        return (tokens, atom_map) if get_atom_indices else tokens

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        '''Creates an drfp array from a reaction SMILES string.
        Arguments:
            in_smiles: A valid reaction SMILES string
            radius: The drfp radius (a radius of 3 corresponds to drfp6)
            min_radius: The minimum radius that is used to extract n-grams
            rings: Whether or not to include rings in the shingling
        Returns:
            A tuple with two arrays, the first containing the drfp hash values, the second the substructure SMILES
        '''
        parts = in_smiles.split('>')
        if len(parts) == 3:
            reactants_part, reagents_part, products_part = parts
        elif len(parts) == 2:
            reactants_part, products_part = parts
            reagents_part = ''
        else:
            reactants_part = parts[0] if parts else ''
            reagents_part = ''
            products_part = ''

        def _mols_from_part(part: str) -> List[Mol]:
            if not part:
                return []
            mols: List[Mol] = []
            for sp in part.split('.'):
                sp = sp.strip()
                if not sp:
                    continue
                m = Chem.MolFromSmiles(sp)
                if m is not None:
                    mols.append(m)
            return mols

        reactant_mols = _mols_from_part(reactants_part)
        reagent_mols = _mols_from_part(reagents_part)
        product_mols = _mols_from_part(products_part)

        def _shingle_side(mols: List[Mol]) -> Tuple[Set[str], List[Dict[str, List[Set[int]]]]]:
            side_tokens: Set[str] = set()
            side_maps: List[Dict[str, List[Set[int]]]] = []
            for m in mols:
                if get_atom_indices:
                    toks, amap = DRFPUtil.shingling_from_mol(
                        m,
                        radius=radius,
                        rings=rings,
                        min_radius=min_radius,
                        get_atom_indices=True,
                        root_central_atom=root_central_atom,
                        include_hydrogens=include_hydrogens,
                    )
                    side_maps.append(amap)
                else:
                    toks = DRFPUtil.shingling_from_mol(
                        m,
                        radius=radius,
                        rings=rings,
                        min_radius=min_radius,
                        get_atom_indices=False,
                        root_central_atom=root_central_atom,
                        include_hydrogens=include_hydrogens,
                    )
                side_tokens.update(toks)
            return side_tokens, side_maps

        left_tokens_react, left_maps_react = _shingle_side(reactant_mols)
        left_tokens_reag, left_maps_reag = _shingle_side(reagent_mols)
        right_tokens_prod, right_maps_prod = _shingle_side(product_mols)

        left_tokens = left_tokens_react.union(left_tokens_reag)
        right_tokens = right_tokens_prod

        symdiff_tokens = sorted(left_tokens.symmetric_difference(right_tokens))
        hashed = DRFPUtil.hash(symdiff_tokens)

        tokens_array = np.array(symdiff_tokens, dtype=object)

        if get_atom_indices:
            mapping_by_side: Dict[str, List[Dict[str, List[Set[int]]]]] = {
                'reactants': left_maps_react,
                'reagents': left_maps_reag,
                'products': right_maps_prod,
            }
            return hashed, tokens_array, mapping_by_side
        else:
            return hashed, tokens_array

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        '''Directly hash all the SMILES in a shingling to a 32-bit integer.
        Arguments:
            shingling: A list of n-grams
        Returns:
            A list of hashed n-grams
        '''
        if not shingling:
            return np.array([], dtype=np.uint32)
        out = np.empty(len(shingling), dtype=np.uint32)
        for i, s in enumerate(shingling):
            if not isinstance(s, str):
                s = str(s)
            digest = hashlib.sha1(s.encode('utf-8')).digest()
            val = int.from_bytes(digest[:4], byteorder='little', signed=False)
            out[i] = np.uint32(val)
        return out

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        '''Folds the hash values to a binary vector of a given length.
        Arguments:
            hash_value: An array containing the hash values
            length: The length of the folded fingerprint
        Returns:
            A tuple containing the folded fingerprint and the indices of the on bits
        '''
        if hash_values is None or hash_values.size == 0:
            return np.zeros(length, dtype=np.uint8), np.array([], dtype=np.int32)
        idx = (hash_values.astype(np.uint64) %
               np.uint64(length)).astype(np.int32)
        uniq_idx = np.unique(idx)
        fp = np.zeros(length, dtype=np.uint8)
        fp[uniq_idx] = 1
        return fp, uniq_idx

    @staticmethod
    def encode(X: Union[Iterable, str], n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False) -> Union[List[np.ndarray], Tuple[List[np.ndarray], Dict[int, Set[str]]], Tuple[List[np.ndarray], Dict[int, Set[str]]], List[Dict[str, List[Dict[str, List[Set[int]]]]]]]:
        '''Encodes a list of reaction SMILES using the drfp fingerprint.
        Args:
            X: An iterable (e.g. List) of reaction SMILES or a single reaction SMILES to be encoded
            n_folded_length: The folded length of the fingerprint (the parameter for the modulo hashing)
            min_radius: The minimum radius of a substructure (0 includes single atoms)
            radius: The maximum radius of a substructure
            rings: Whether to include full rings as substructures
            mapping: Return a feature to substructure mapping in addition to the fingerprints
            atom_index_mapping: Return the atom indices of mapped substructures for each reaction
            root_central_atom: Whether to root the central atom of substructures when generating SMILES
            show_progress_bar: Whether to show a progress bar when encoding reactions
        Returns:
            A list of drfp fingerprints or, if mapping is enabled, a tuple containing a list of drfp fingerprints and a mapping dict.
        '''
        if isinstance(X, str):
            iterable: List[str] = [X]
        else:
            iterable = list(X)

        fps: List[np.ndarray] = []
        feature_map: Dict[int, Set[str]] = {}
        atom_maps_all: List[Dict[str, List[Dict[str, List[Set[int]]]]]] = []

        total = len(iterable)
        for i, rxn in enumerate(iterable):
            if atom_index_mapping:
                hv, toks, atom_map = DRFPUtil.internal_encode(
                    rxn,
                    radius=radius,
                    min_radius=min_radius,
                    rings=rings,
                    get_atom_indices=True,
                    root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens,
                )
                atom_maps_all.append(atom_map)  # type: ignore[arg-type]
            else:
                hv, toks = DRFPUtil.internal_encode(
                    rxn,
                    radius=radius,
                    min_radius=min_radius,
                    rings=rings,
                    get_atom_indices=False,
                    root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens,
                )
            fp, idx = DRFPUtil.fold(hv, length=n_folded_length)
            fps.append(fp)

            if mapping and not atom_index_mapping:
                if toks.size > 0:
                    fold_idx = (hv.astype(np.uint64) %
                                np.uint64(n_folded_length)).astype(np.int32)
                    for j, fidx in enumerate(fold_idx):
                        token = str(toks[j])
                        s = feature_map.get(int(fidx))
                        if s is None:
                            feature_map[int(fidx)] = {token}
                        else:
                            s.add(token)

            if show_progress_bar:
                pass  # Intentionally no output to keep function silent in non-interactive usage

        if atom_index_mapping:
            return atom_maps_all
        if mapping:
            return fps, feature_map
        return fps
