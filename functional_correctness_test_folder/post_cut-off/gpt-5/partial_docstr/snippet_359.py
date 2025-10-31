from typing import Dict, Iterable, List, Set, Tuple, Union
import numpy as np

try:
    from rdkit import Chem
    from rdkit.Chem import rdchem
except ImportError as e:
    Chem = None
    rdchem = None

Mol = rdchem.Mol if rdchem is not None else object


class DRFPUtil:
    @staticmethod
    def _ensure_mol(m: Union[str, Mol]) -> Mol:
        if isinstance(m, str):
            mol = Chem.MolFromSmiles(m)
            if mol is None:
                raise ValueError(f"Invalid SMILES: {m}")
            return mol
        return m

    @staticmethod
    def _get_ring_atom_sets(mol: Mol) -> List[Set[int]]:
        ri = mol.GetRingInfo()
        atom_rings = ri.AtomRings()
        return [set(r) for r in atom_rings]

    @staticmethod
    def _fragment_smiles(
        mol: Mol,
        atoms: List[int],
        rooted_at: Union[int, None],
        include_hydrogens: bool,
    ) -> str:
        rooted = rooted_at if rooted_at is not None and rooted_at in atoms else -1
        return Chem.MolFragmentToSmiles(
            mol,
            atomsToUse=atoms,
            rootedAtAtom=rooted,
            allHsExplicit=include_hydrogens,
            allBondsExplicit=True,
            isomericSmiles=True,
            canonical=True,
        )

    @staticmethod
    def shingling_from_mol(
        in_mol: Mol,
        radius: int = 3,
        rings: bool = True,
        min_radius: int = 0,
        get_atom_indices: bool = False,
        root_central_atom: bool = True,
        include_hydrogens: bool = False,
    ) -> Union[List[str], Tuple[List[str], Dict[str, List[Set[int]]]]]:
        mol = DRFPUtil._ensure_mol(in_mol)

        if include_hydrogens:
            mol = Chem.AddHs(mol)
        shingles: List[str] = []
        mapping: Dict[str, List[Set[int]]] = {}

        # Circular neighborhoods
        n_atoms = mol.GetNumAtoms()
        for a in range(n_atoms):
            for r in range(min_radius, radius + 1):
                if r == 0:
                    atom_set = {a}
                else:
                    bond_ids = Chem.FindAtomEnvironmentOfRadiusN(mol, r, a)
                    if not bond_ids:
                        continue
                    atom_set = set()
                    for bidx in bond_ids:
                        b = mol.GetBondWithIdx(bidx)
                        atom_set.add(b.GetBeginAtomIdx())
                        atom_set.add(b.GetEndAtomIdx())
                atoms = sorted(atom_set)
                rooted = a if root_central_atom else None
                smi = DRFPUtil._fragment_smiles(
                    mol, atoms, rooted, include_hydrogens)
                shingles.append(smi)
                if get_atom_indices:
                    mapping.setdefault(smi, []).append(set(atom_set))

        # Rings
        if rings:
            for ring in DRFPUtil._get_ring_atom_sets(mol):
                atoms = sorted(ring)
                smi = DRFPUtil._fragment_smiles(
                    mol, atoms, None, include_hydrogens)
                shingles.append(smi)
                if get_atom_indices:
                    mapping.setdefault(smi, []).append(set(ring))

        if get_atom_indices:
            return shingles, mapping
        return shingles

    @staticmethod
    def _reaction_sides_from_smiles(in_smiles: str) -> Tuple[List[Mol], List[Mol]]:
        parts = in_smiles.split(">")
        if len(parts) == 3:
            left = parts[0]
            right = parts[2]
        elif ">>" in in_smiles:
            left, right = in_smiles.split(">>", 1)
        else:
            # Treat as a single molecule to "product", with empty left
            left, right = "", in_smiles

        def parse_side(s: str) -> List[Mol]:
            if not s:
                return []
            parts = [p for p in s.split(".") if p]
            mols: List[Mol] = []
            for p in parts:
                m = Chem.MolFromSmiles(p)
                if m is None:
                    raise ValueError(
                        f"Invalid component SMILES in reaction: {p}")
                mols.append(m)
            return mols

        left_mols = parse_side(left)
        right_mols = parse_side(right)
        return left_mols, right_mols

    @staticmethod
    def _count_shingles(shingles: List[str]) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for s in shingles:
            counts[s] = counts.get(s, 0) + 1
        return counts

    @staticmethod
    def internal_encode(
        in_smiles: str,
        radius: int = 3,
        min_radius: int = 0,
        rings: bool = True,
        get_atom_indices: bool = False,
        root_central_atom: bool = True,
        include_hydrogens: bool = False,
    ) -> Union[
        Tuple[np.ndarray, np.ndarray],
        Tuple[np.ndarray, np.ndarray, Dict[str, List[Dict[str, List[Set[int]]]]]],
    ]:
        if Chem is None:
            raise ImportError("rdkit is required for DRFPUtil")

        left_mols, right_mols = DRFPUtil._reaction_sides_from_smiles(in_smiles)

        left_shingles: List[str] = []
        right_shingles: List[str] = []
        left_maps: List[Dict[str, List[Set[int]]]] = []
        right_maps: List[Dict[str, List[Set[int]]]] = []

        for m in left_mols:
            res = DRFPUtil.shingling_from_mol(
                m,
                radius=radius,
                rings=rings,
                min_radius=min_radius,
                get_atom_indices=get_atom_indices,
                root_central_atom=root_central_atom,
                include_hydrogens=include_hydrogens,
            )
            if get_atom_indices:
                shingles, amap = res  # type: ignore
                left_maps.append(amap)
            else:
                shingles = res  # type: ignore
            left_shingles.extend(shingles)  # type: ignore

        for m in right_mols:
            res = DRFPUtil.shingling_from_mol(
                m,
                radius=radius,
                rings=rings,
                min_radius=min_radius,
                get_atom_indices=get_atom_indices,
                root_central_atom=root_central_atom,
                include_hydrogens=include_hydrogens,
            )
            if get_atom_indices:
                shingles, amap = res  # type: ignore
                right_maps.append(amap)
            else:
                shingles = res  # type: ignore
            right_shingles.extend(shingles)  # type: ignore

        # Multiset symmetric difference: retain shingles with different counts across sides
        left_counts = DRFPUtil._count_shingles(left_shingles)
        right_counts = DRFPUtil._count_shingles(right_shingles)

        diff_shingles: List[str] = []
        keys = set(left_counts.keys()) | set(right_counts.keys())
        for k in keys:
            cnt = abs(right_counts.get(k, 0) - left_counts.get(k, 0))
            if cnt > 0:
                diff_shingles.extend([k] * cnt)

        hashed = DRFPUtil.hash(diff_shingles)
        folded_vec, _ = DRFPUtil.fold(hashed)

        if get_atom_indices:
            mapping = {"reactants": left_maps, "products": right_maps}
            return hashed, folded_vec, mapping
        return hashed, folded_vec

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        # Stable hash via SHA1, 64-bit unsigned integers
        import hashlib

        vals = np.empty(len(shingling), dtype=np.uint64)
        for i, s in enumerate(shingling):
            h = hashlib.sha1(s.encode("utf-8")).digest()
            # take first 8 bytes as unsigned 64-bit
            vals[i] = int.from_bytes(h[:8], byteorder="big", signed=False)
        return vals

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        if length <= 0:
            raise ValueError("length must be positive")
        idxs = (hash_values % np.uint64(length)).astype(np.int64)
        vec = np.zeros(length, dtype=np.float32)
        # count occurrences
        np.add.at(vec, idxs, 1.0)
        return vec, idxs

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
        show_progress_bar: bool = False,
    ) -> Union[
        List[np.ndarray],
        Tuple[List[np.ndarray], Dict[int, Set[str]]],
        Tuple[List[np.ndarray], Dict[int, Set[str]]],
        List[Dict[str, List[Dict[str, List[Set[int]]]]]],
    ]:
        if Chem is None:
            raise ImportError("rdkit is required for DRFPUtil")

        if isinstance(X, str):
            X_iter = [X]
        else:
            X_iter = list(X)

        fingerprints: List[np.ndarray] = []
        feature_to_bin_map: Dict[int, Set[str]] = {}

        # Optional progress
        iterator = X_iter
        if show_progress_bar:
            try:
                from tqdm import tqdm  # type: ignore
                iterator = tqdm(X_iter)
            except Exception:
                pass

        if atom_index_mapping and not mapping:
            # Return atom index mappings per reaction
            all_idx_maps: List[Dict[str, List[Dict[str, List[Set[int]]]]]] = []
            for rxn in iterator:
                _, _, idx_map = DRFPUtil.internal_encode(
                    rxn,
                    radius=radius,
                    min_radius=min_radius,
                    rings=rings,
                    get_atom_indices=True,
                    root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens,
                )
                all_idx_maps.append(idx_map)  # type: ignore
            return all_idx_maps

        for rxn in iterator:
            # get hashed and folded vector
            hashed, vec = DRFPUtil.internal_encode(
                rxn,
                radius=radius,
                min_radius=min_radius,
                rings=rings,
                get_atom_indices=False,
                root_central_atom=root_central_atom,
                include_hydrogens=include_hydrogens,
            )
            # Ensure folding length matches desired n_folded_length
            if len(vec) != n_folded_length:
                folded_vec, _ = DRFPUtil.fold(hashed, length=n_folded_length)
                fingerprints.append(folded_vec)
            else:
                fingerprints.append(vec)

            if mapping:
                # Recompute diff shingles to populate feature mapping to bins
                left_mols, right_mols = DRFPUtil._reaction_sides_from_smiles(
                    rxn)
                left_sh: List[str] = []
                right_sh: List[str] = []
                for m in left_mols:
                    left_sh.extend(
                        DRFPUtil.shingling_from_mol(
                            m,
                            radius=radius,
                            rings=rings,
                            min_radius=min_radius,
                            get_atom_indices=False,
                            root_central_atom=root_central_atom,
                            include_hydrogens=include_hydrogens,
                        )
                    )
                for m in right_mols:
                    right_sh.extend(
                        DRFPUtil.shingling_from_mol(
                            m,
                            radius=radius,
                            rings=rings,
                            min_radius=min_radius,
                            get_atom_indices=False,
                            root_central_atom=root_central_atom,
                            include_hydrogens=include_hydrogens,
                        )
                    )
                lc = DRFPUtil._count_shingles(left_sh)
                rc = DRFPUtil._count_shingles(right_sh)
                diff: List[str] = []
                for k in set(lc) | set(rc):
                    cnt = abs(rc.get(k, 0) - lc.get(k, 0))
                    if cnt:
                        diff.extend([k] * cnt)
                hv = DRFPUtil.hash(diff)
                bins = (hv % np.uint64(n_folded_length)).astype(np.int64)
                for s, b in zip(diff, bins):
                    feature_to_bin_map.setdefault(int(b), set()).add(s)

        if mapping:
            return fingerprints, feature_to_bin_map
        return fingerprints
