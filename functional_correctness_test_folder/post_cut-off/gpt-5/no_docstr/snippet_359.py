from typing import Dict, Iterable, List, Set, Tuple, Union

import hashlib
import numpy as np
from rdkit import Chem
from rdkit.Chem import Mol
from rdkit.Chem import rdchem
from rdkit.Chem import rdMolDescriptors


class DRFPUtil:
    @staticmethod
    def _safe_mol_from_smiles(smiles: str, include_hydrogens: bool = False) -> Union[Mol, None]:
        if not isinstance(smiles, str):
            return None
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        if include_hydrogens:
            mol = Chem.AddHs(mol, addCoords=False)
        return mol

    @staticmethod
    def _env_atom_indices(mol: Mol, center: int, radius: int) -> Set[int]:
        if radius == 0:
            return {center}
        bond_ids = Chem.FindAtomEnvironmentOfRadiusN(mol, radius, center)
        atom_ids: Set[int] = set()
        for bid in bond_ids:
            b = mol.GetBondWithIdx(bid)
            atom_ids.add(b.GetBeginAtomIdx())
            atom_ids.add(b.GetEndAtomIdx())
        # also include the center atom even if isolated by ring shortcuts
        atom_ids.add(center)
        return atom_ids

    @staticmethod
    def _fragment_smiles(
        mol: Mol,
        atom_indices: Set[int],
        rooted_at: Union[int, None] = None,
        canonical: bool = True,
        isomeric: bool = True,
    ) -> str:
        if not atom_indices:
            return ""
        try:
            atms = sorted(atom_indices)
            return Chem.MolFragmentToSmiles(
                mol,
                atomsToUse=atms,
                rootedAtAtom=rooted_at if rooted_at is not None else -1,
                canonical=canonical,
                isomericSmiles=isomeric,
            )
        except Exception:
            # robust fallback: sanitize a submol
            try:
                amap = {}
                sub = Chem.PathToSubmol(mol, [])
                return Chem.MolToSmiles(sub, canonical=canonical, isomericSmiles=isomeric)
            except Exception:
                return ""

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
        if in_mol is None:
            return ([], {}) if get_atom_indices else []

        mol = in_mol
        if include_hydrogens:
            mol = Chem.AddHs(mol, addCoords=False)

        shingles: List[str] = []
        mapping: Dict[str, List[Set[int]]] = {}

        n_atoms = mol.GetNumAtoms()
        min_r = max(0, int(min_radius))
        max_r = max(min_r, int(radius))

        for aidx in range(n_atoms):
            for r in range(min_r, max_r + 1):
                atom_set = DRFPUtil._env_atom_indices(mol, aidx, r)
                if not atom_set:
                    continue
                s = DRFPUtil._fragment_smiles(
                    mol,
                    atom_set,
                    rooted_at=aidx if root_central_atom else None,
                )
                if not s:
                    continue
                shingles.append(s)
                if get_atom_indices:
                    mapping.setdefault(s, []).append(set(atom_set))

        if rings:
            ri = mol.GetRingInfo()
            try:
                bond_rings = ri.BondRings()
                for bond_ring in bond_rings:
                    atoms_in_ring: Set[int] = set()
                    for bid in bond_ring:
                        b = mol.GetBondWithIdx(bid)
                        atoms_in_ring.add(b.GetBeginAtomIdx())
                        atoms_in_ring.add(b.GetEndAtomIdx())
                    s = DRFPUtil._fragment_smiles(
                        mol,
                        atoms_in_ring,
                        rooted_at=None,
                    )
                    if s:
                        shingles.append(s)
                        if get_atom_indices:
                            mapping.setdefault(s, []).append(
                                set(atoms_in_ring))
            except Exception:
                # Fallback via AtomRings if BondRings not available
                try:
                    atom_rings = ri.AtomRings()
                    for atom_ring in atom_rings:
                        atoms_in_ring = set(atom_ring)
                        s = DRFPUtil._fragment_smiles(
                            mol, atoms_in_ring, rooted_at=None)
                        if s:
                            shingles.append(s)
                            if get_atom_indices:
                                mapping.setdefault(s, []).append(
                                    set(atoms_in_ring))
                except Exception:
                    pass

        return (shingles, mapping) if get_atom_indices else shingles

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
        mol = DRFPUtil._safe_mol_from_smiles(
            in_smiles, include_hydrogens=include_hydrogens)
        if mol is None:
            folded = np.zeros((2048,), dtype=np.int32)
            positions = np.array([], dtype=np.int64)
            if get_atom_indices:
                return folded, positions, {"atom_index_mapping": []}
            return folded, positions

        shingles_out = DRFPUtil.shingling_from_mol(
            mol,
            radius=radius,
            rings=rings,
            min_radius=min_radius,
            get_atom_indices=get_atom_indices,
            root_central_atom=root_central_atom,
            include_hydrogens=include_hydrogens,
        )

        if get_atom_indices:
            shingles, atom_map = shingles_out  # type: ignore
        else:
            shingles = shingles_out  # type: ignore
            atom_map = None

        h = DRFPUtil.hash(shingles) if shingles else np.array(
            [], dtype=np.uint64)
        folded, positions = DRFPUtil.fold(h, length=2048)

        if get_atom_indices:
            return folded, positions, {"atom_index_mapping": [atom_map if atom_map is not None else {}]}
        return folded, positions

    @staticmethod
    def hash(shingling: List[str]) -> np.ndarray:
        if not shingling:
            return np.array([], dtype=np.uint64)

        hashes = np.empty(len(shingling), dtype=np.uint64)
        for i, s in enumerate(shingling):
            # deterministic 32-bit hash via sha1 digest
            digest = hashlib.sha1(s.encode("utf-8")).digest()
            val = int.from_bytes(digest[:8], byteorder="little", signed=False)
            hashes[i] = np.uint64(val)
        return hashes

    @staticmethod
    def fold(hash_values: np.ndarray, length: int = 2048) -> Tuple[np.ndarray, np.ndarray]:
        L = int(length)
        if L <= 0:
            raise ValueError("length must be positive")
        folded = np.zeros((L,), dtype=np.int32)
        if hash_values is None or hash_values.size == 0:
            return folded, np.array([], dtype=np.int64)
        idx = (hash_values % np.uint64(L)).astype(np.int64)
        # simple count folding
        for i in idx:
            folded[int(i)] += 1
        return folded, idx

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
        if isinstance(X, str):
            iterable = [X]
        else:
            iterable = list(X)

        fps: List[np.ndarray] = []
        idx_to_shingles: Dict[int, Set[str]] = {}
        atom_maps_all: List[Dict[str, List[Dict[str, List[Set[int]]]]]] = []

        for i, smi in enumerate(iterable):
            mol = DRFPUtil._safe_mol_from_smiles(
                str(smi), include_hydrogens=include_hydrogens)
            if mol is None:
                fps.append(np.zeros((n_folded_length,), dtype=np.int32))
                if mapping:
                    idx_to_shingles[i] = set()
                if atom_index_mapping:
                    atom_maps_all.append({"atom_index_mapping": []})
                continue

            shingles_out = DRFPUtil.shingling_from_mol(
                mol,
                radius=radius,
                rings=rings,
                min_radius=min_radius,
                get_atom_indices=atom_index_mapping,
                root_central_atom=root_central_atom,
                include_hydrogens=include_hydrogens,
            )

            if atom_index_mapping:
                shingles, atom_map = shingles_out  # type: ignore
            else:
                shingles = shingles_out  # type: ignore
                atom_map = None

            if mapping:
                idx_to_shingles[i] = set(shingles)

            h = DRFPUtil.hash(shingles) if shingles else np.array(
                [], dtype=np.uint64)
            folded, _ = DRFPUtil.fold(h, length=n_folded_length)
            fps.append(folded)

            if atom_index_mapping:
                atom_maps_all.append(
                    {"atom_index_mapping": [atom_map if atom_map is not None else {}]})

        if atom_index_mapping:
            return atom_maps_all
        if mapping:
            return fps, idx_to_shingles
        return fps
