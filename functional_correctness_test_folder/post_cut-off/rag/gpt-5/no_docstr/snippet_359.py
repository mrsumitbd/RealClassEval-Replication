import numpy as np
from typing import Union, List, Tuple, Dict, Set, Iterable
from collections import Counter, defaultdict
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

        shingling: List[str] = []
        indices_map: Dict[str, List[Set[int]]] = defaultdict(list)

        max_r = max(0, int(radius))
        min_r = max(0, int(min_radius))
        if min_r > max_r:
            min_r = max_r

        n_atoms = in_mol.GetNumAtoms()
        for center in range(n_atoms):
            for r in range(min_r, max_r + 1):
                env_bonds = Chem.FindAtomEnvironmentOfRadiusN(
                    in_mol, r, center)
                if r == 0:
                    atoms = {center}
                    bonds_to_use = None
                else:
                    atom_set: Set[int] = set([center])
                    for b_idx in env_bonds:
                        b = in_mol.GetBondWithIdx(b_idx)
                        atom_set.add(b.GetBeginAtomIdx())
                        atom_set.add(b.GetEndAtomIdx())
                    atoms = atom_set
                    bonds_to_use = env_bonds

                rootedAtAtom = center if root_central_atom else -1
                try:
                    frag_smiles = Chem.MolFragmentToSmiles(
                        in_mol,
                        atomsToUse=sorted(list(atoms)),
                        bondsToUse=bonds_to_use,
                        rootedAtAtom=rootedAtAtom,
                        canonical=True,
                        isomericSmiles=True,
                        allHsExplicit=include_hydrogens
                    )
                except Exception:
                    continue

                shingling.append(frag_smiles)
                if get_atom_indices:
                    indices_map[frag_smiles].append(set(atoms))

        if rings:
            ring_info = in_mol.GetRingInfo()
            # Use bond rings to ensure full rings are captured
            for ring_bond_indices in ring_info.BondRings():
                ring_atoms: Set[int] = set()
                for b_idx in ring_bond_indices:
                    b = in_mol.GetBondWithIdx(b_idx)
                    ring_atoms.add(b.GetBeginAtomIdx())
                    ring_atoms.add(b.GetEndAtomIdx())
                root_atom = min(ring_atoms) if root_central_atom else -1
                try:
                    ring_smiles = Chem.MolFragmentToSmiles(
                        in_mol,
                        atomsToUse=sorted(list(ring_atoms)),
                        bondsToUse=list(ring_bond_indices),
                        rootedAtAtom=root_atom,
                        canonical=True,
                        isomericSmiles=True,
                        allHsExplicit=include_hydrogens
                    )
                except Exception:
                    ring_smiles = None
                if ring_smiles:
                    shingling.append(ring_smiles)
                    if get_atom_indices:
                        indices_map[ring_smiles].append(set(ring_atoms))

        if get_atom_indices:
            return shingling, dict(indices_map)
        return shingling

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
        if not isinstance(in_smiles, str):
            if get_atom_indices:
                return np.array([], dtype=np.uint32), np.array([], dtype=object), {'left': [], 'right': []}
            return np.array([], dtype=np.uint32), np.array([], dtype=object)

        # Parse reaction SMILES: reactants>reagents>products
        parts = in_smiles.split('>')
        if len(parts) == 3:
            left_str = parts[0]
            reagents_str = parts[1]
            right_str = parts[2]
            left_full = left_str if not reagents_str else (
                left_str + ('.' if left_str and reagents_str else '') + reagents_str)
        elif len(parts) == 2:  # fallback: reactants>>products
            left_full = parts[0]
            right_str = parts[1]
        else:  # treat as a molecule, products only
            left_full = ""
            right_str = parts[0]

        def smiles_to_mols(s: str) -> List[Mol]:
            s = s.strip()
            if not s:
                return []
            mols = []
            for sp in s.split('.'):
                sp = sp.strip()
                if not sp:
                    continue
                m = Chem.MolFromSmiles(sp)
                if m is not None:
                    mols.append(m)
            return mols

        left_mols = smiles_to_mols(left_full)
        right_mols = smiles_to_mols(right_str)

        left_shingles: List[str] = []
        right_shingles: List[str] = []

        left_atom_maps: List[Dict[str, List[Set[int]]]] = []
        right_atom_maps: List[Dict[str, List[Set[int]]]] = []

        for m in left_mols:
            if get_atom_indices:
                s, idx_map = DRFPUtil.shingling_from_mol(
                    m, radius=radius, rings=rings, min_radius=min_radius,
                    get_atom_indices=True, root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                left_shingles.extend(s)
                left_atom_maps.append(idx_map)
            else:
                s = DRFPUtil.shingling_from_mol(
                    m, radius=radius, rings=rings, min_radius=min_radius,
                    get_atom_indices=False, root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                left_shingles.extend(s)  # type: ignore[arg-type]

        for m in right_mols:
            if get_atom_indices:
                s, idx_map = DRFPUtil.shingling_from_mol(
                    m, radius=radius, rings=rings, min_radius=min_radius,
                    get_atom_indices=True, root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                right_shingles.extend(s)
                right_atom_maps.append(idx_map)
            else:
                s = DRFPUtil.shingling_from_mol(
                    m, radius=radius, rings=rings, min_radius=min_radius,
                    get_atom_indices=False, root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                right_shingles.extend(s)  # type: ignore[arg-type]

        # Multiset symmetric difference: include each feature |count_left - count_right| times
        c_left = Counter(left_shingles)
        c_right = Counter(right_shingles)
        all_keys = set(c_left.keys()) | set(c_right.keys())
        diff_shingles: List[str] = []
        for k in all_keys:
            n = abs(c_left.get(k, 0) - c_right.get(k, 0))
            if n > 0:
                diff_shingles.extend([k] * n)

        if len(diff_shingles) == 0:
            if get_atom_indices:
                return np.array([], dtype=np.uint32), np.array([], dtype=object), {'left': left_atom_maps, 'right': right_atom_maps}
            return np.array([], dtype=np.uint32), np.array([], dtype=object)

        hash_vals = DRFPUtil.hash(diff_shingles)
        smiles_arr = np.array(diff_shingles, dtype=object)
        if get_atom_indices:
            return hash_vals, smiles_arr, {'left': left_atom_maps, 'right': right_atom_maps}
        return hash_vals, smiles_arr

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
            h = hashlib.sha1(s.encode('utf-8')).digest()
            # take first 4 bytes as unsigned 32-bit integer (big-endian)
            out[i] = int.from_bytes(h[:4], byteorder='big', signed=False)
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
        if hash_values is None or len(hash_values) == 0 or length <= 0:
            return np.zeros((max(0, length),), dtype=np.uint8), np.array([], dtype=np.int64)
        idx = np.mod(hash_values.astype(np.uint64),
                     np.uint64(length)).astype(np.int64)
        # Ensure uniqueness of active bits
        unique_idx = np.unique(idx)
        fp = np.zeros((length,), dtype=np.uint8)
        fp[unique_idx] = 1
        return fp, unique_idx

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
        # Normalize input to iterable of strings
        if isinstance(X, str):
            smiles_list = [X]
        else:
            smiles_list = list(X)

        fps: List[np.ndarray] = []
        feat_map: Dict[int, Set[str]] = defaultdict(set)
        atom_maps_per_rxn: List[Dict[str,
                                     List[Dict[str, List[Set[int]]]]]] = []

        iterator = smiles_list
        if show_progress_bar:
            try:
                from tqdm.auto import tqdm  # type: ignore
                iterator = tqdm(smiles_list, desc="Encoding DRFP")
            except Exception:
                pass

        for rxn in iterator:
            if atom_index_mapping:
                hv, strs, side_maps = DRFPUtil.internal_encode(
                    rxn, radius=radius, min_radius=min_radius, rings=rings,
                    get_atom_indices=True, root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
                atom_maps_per_rxn.append(side_maps)
            else:
                hv, strs = DRFPUtil.internal_encode(
                    rxn, radius=radius, min_radius=min_radius, rings=rings,
                    get_atom_indices=False, root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )

            fp, idx = DRFPUtil.fold(hv, length=n_folded_length)
            fps.append(fp)

            if mapping and len(hv) > 0:
                # map each bit index to the set of substructures (strings) that landed there
                # We recompute indices per feature to avoid collision ambiguity
                for s in strs:
                    h = DRFPUtil.hash([s])[0]
                    bit = int(h % np.uint64(n_folded_length))
                    feat_map[bit].add(s)

        if mapping:
            return fps, dict(feat_map)

        if atom_index_mapping:
            return atom_maps_per_rxn

        return fps
