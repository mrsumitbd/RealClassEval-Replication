import numpy as np
from typing import List, Tuple, Dict, Set, Union, Iterable
from collections import Counter, defaultdict
import hashlib

from rdkit import Chem
from rdkit.Chem.rdchem import Mol


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

        mol = Chem.Mol(in_mol)
        if include_hydrogens:
            mol = Chem.AddHs(mol, addCoords=False)

        shingles: List[str] = []
        idx_map: Dict[str, List[Set[int]]] = defaultdict(
            list) if get_atom_indices else {}

        # Atom-centered environments
        for atom in mol.GetAtoms():
            if not include_hydrogens and atom.GetAtomicNum() == 1:
                continue
            a_idx = atom.GetIdx()
            for r in range(max(0, min_radius), max(min_radius, radius) + 1):
                if r == 0:
                    atoms_in_env = {a_idx}
                    bonds_in_env: List[int] = []
                else:
                    bonds_in_env = list(
                        Chem.FindAtomEnvironmentOfRadiusN(mol, r, a_idx))
                    if not bonds_in_env:
                        continue
                    atoms_in_env = set()
                    for bidx in bonds_in_env:
                        b = mol.GetBondWithIdx(bidx)
                        atoms_in_env.add(b.GetBeginAtomIdx())
                        atoms_in_env.add(b.GetEndAtomIdx())

                try:
                    frag_smiles = Chem.MolFragmentToSmiles(
                        mol,
                        atomsToUse=sorted(list(atoms_in_env)),
                        bondsToUse=bonds_in_env if bonds_in_env else None,
                        rootedAtAtom=(a_idx if root_central_atom else -1),
                        isomericSmiles=True,
                        canonical=True,
                        kekuleSmiles=False,
                        allBondsExplicit=False,
                        allHsExplicit=include_hydrogens
                    )
                except Exception:
                    continue

                if frag_smiles:
                    shingles.append(frag_smiles)
                    if get_atom_indices:
                        idx_map[frag_smiles].append(set(atoms_in_env))

        # Ring features
        if rings:
            ring_info = mol.GetRingInfo()
            if ring_info is not None:
                for bond_ring in ring_info.BondRings():
                    bond_ring_list = list(bond_ring)
                    ring_atom_indices: Set[int] = set()
                    for bidx in bond_ring_list:
                        b = mol.GetBondWithIdx(bidx)
                        ring_atom_indices.add(b.GetBeginAtomIdx())
                        ring_atom_indices.add(b.GetEndAtomIdx())
                    rooted = min(
                        ring_atom_indices) if root_central_atom and ring_atom_indices else -1
                    try:
                        ring_smiles = Chem.MolFragmentToSmiles(
                            mol,
                            atomsToUse=sorted(list(ring_atom_indices)),
                            bondsToUse=bond_ring_list if bond_ring_list else None,
                            rootedAtAtom=rooted,
                            isomericSmiles=True,
                            canonical=True,
                            kekuleSmiles=False,
                            allBondsExplicit=False,
                            allHsExplicit=include_hydrogens
                        )
                    except Exception:
                        ring_smiles = None
                    if ring_smiles:
                        shingles.append(ring_smiles)
                        if get_atom_indices:
                            idx_map[ring_smiles].append(set(ring_atom_indices))

        return (shingles, dict(idx_map)) if get_atom_indices else shingles

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
        if in_smiles is None:
            empty = np.array([], dtype=np.uint32), np.array([], dtype=object)
            if get_atom_indices:
                return empty[0], empty[1], {'left': [], 'right': []}
            return empty

        parts = in_smiles.split('>')
        if len(parts) == 2:
            left_str, right_str = parts[0], parts[1]
            mid_str = ""
        elif len(parts) >= 3:
            left_str, mid_str, right_str = parts[0], parts[1], parts[2]
        else:
            left_str, mid_str, right_str = in_smiles, "", ""

        left_side = '.'.join(p for p in [left_str, mid_str] if p)
        right_side = right_str

        def parse_side(s: str) -> List[Mol]:
            if not s:
                return []
            mols: List[Mol] = []
            for smi in s.split('.'):
                if not smi:
                    continue
                m = Chem.MolFromSmiles(smi)
                if m is not None:
                    mols.append(m)
            return mols

        left_mols = parse_side(left_side)
        right_mols = parse_side(right_side)

        left_shingles: List[str] = []
        right_shingles: List[str] = []

        left_idx_map_list: List[Dict[str, List[Set[int]]]] = []
        right_idx_map_list: List[Dict[str, List[Set[int]]]] = []

        for m in left_mols:
            if get_atom_indices:
                sh, idx_map = DRFPUtil.shingling_from_mol(
                    m, radius=radius, rings=rings, min_radius=min_radius,
                    get_atom_indices=True, root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                left_shingles.extend(sh)
                left_idx_map_list.append(idx_map)
            else:
                sh = DRFPUtil.shingling_from_mol(
                    m, radius=radius, rings=rings, min_radius=min_radius,
                    get_atom_indices=False, root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                left_shingles.extend(sh)  # type: ignore[arg-type]

        for m in right_mols:
            if get_atom_indices:
                sh, idx_map = DRFPUtil.shingling_from_mol(
                    m, radius=radius, rings=rings, min_radius=min_radius,
                    get_atom_indices=True, root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                right_shingles.extend(sh)
                right_idx_map_list.append(idx_map)
            else:
                sh = DRFPUtil.shingling_from_mol(
                    m, radius=radius, rings=rings, min_radius=min_radius,
                    get_atom_indices=False, root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                right_shingles.extend(sh)  # type: ignore[arg-type]

        left_counts = Counter(left_shingles)
        right_counts = Counter(right_shingles)

        all_keys = set(left_counts.keys()) | set(right_counts.keys())
        diff_shingles: List[str] = []
        for k in all_keys:
            n = abs(right_counts.get(k, 0) - left_counts.get(k, 0))
            if n > 0:
                diff_shingles.extend([k] * n)

        hash_values = DRFPUtil.hash(diff_shingles)
        substruct_array = np.array(diff_shingles, dtype=object)

        if get_atom_indices:
            mapping = {'left': left_idx_map_list, 'right': right_idx_map_list}
            return hash_values, substruct_array, mapping

        return hash_values, substruct_array

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        '''Directly hash all the SMILES in a shingling to a 32-bit integer.
        Arguments:
            shingling: A list of n-grams
        Returns:
            A list of hashed n-grams
        '''
        hashes = np.empty(len(shingling), dtype=np.uint32)
        for i, s in enumerate(shingling):
            h = hashlib.sha1(s.encode('utf-8')).digest()
            # first 4 bytes -> 32-bit little-endian unsigned int
            hashes[i] = int.from_bytes(h[:4], byteorder='little', signed=False)
        return hashes

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        '''Folds the hash values to a binary vector of a given length.
        Arguments:
            hash_value: An array containing the hash values
            length: The length of the folded fingerprint
        Returns:
            A tuple containing the folded fingerprint and the indices of the on bits
        '''
        if hash_values.size == 0:
            return np.zeros(length, dtype=np.uint8), np.array([], dtype=np.int64)
        positions = hash_values % np.uint32(length)
        on_idx = np.unique(positions.astype(np.int64, copy=False))
        fp = np.zeros(length, dtype=np.uint8)
        fp[on_idx] = 1
        return fp, on_idx

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
        # Normalize input to list of strings
        if isinstance(X, str):
            rxn_list = [X]
        else:
            rxn_list = list(X)

        try:
            from tqdm.auto import tqdm  # type: ignore
            iterator = tqdm(rxn_list) if show_progress_bar else rxn_list
        except Exception:
            iterator = rxn_list

        fps: List[np.ndarray] = []
        feature_map: Dict[int, Set[str]] = defaultdict(set) if mapping else {}
        atom_idx_maps_per_rxn: List[Dict[str,
                                         List[Dict[str, List[Set[int]]]]]] = []

        for rxn in iterator:
            if atom_index_mapping:
                hv, subs, idx_map = DRFPUtil.internal_encode(
                    rxn,
                    radius=radius,
                    min_radius=min_radius,
                    rings=rings,
                    get_atom_indices=True,
                    root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                atom_idx_maps_per_rxn.append(idx_map)  # type: ignore[arg-type]
            else:
                hv, subs = DRFPUtil.internal_encode(
                    rxn,
                    radius=radius,
                    min_radius=min_radius,
                    rings=rings,
                    get_atom_indices=False,
                    root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )

            fp, _ = DRFPUtil.fold(hv, length=n_folded_length)
            fps.append(fp)

            if mapping:
                if subs.size > 0:
                    positions = (hv % np.uint32(n_folded_length)
                                 ).astype(np.int64, copy=False)
                    for pos, sub in zip(positions.tolist(), subs.tolist()):
                        feature_map[pos].add(sub)  # type: ignore[index]

        if mapping:
            return fps, feature_map  # type: ignore[return-value]
        if atom_index_mapping:
            return atom_idx_maps_per_rxn
        return fps
