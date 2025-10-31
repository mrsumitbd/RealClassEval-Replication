class DRFPUtil:
    '''
    A utility class for encoding SMILES as drfp fingerprints.
    '''
    @staticmethod
    def shingling_from_mol(in_mol, radius: int = 3, rings: bool = True, min_radius: int = 0, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False):
        '''Creates a molecular shingling from a RDKit molecule (rdkit.Chem.rdchem.Mol).
        Arguments:
            in_mol: A RDKit molecule instance
            radius: The drfp radius (a radius of 3 corresponds to drfp6)
            rings: Whether or not to include rings in the shingling
            min_radius: The minimum radius that is used to extract n-grams
        Returns:
            The molecular shingling.
        '''
        from rdkit import Chem
        from rdkit.Chem import rdMolDescriptors

        if in_mol is None:
            return [] if not get_atom_indices else ([], {})

        mol = Chem.Mol(in_mol)
        if include_hydrogens:
            mol = Chem.AddHs(mol)
        shingling: list[str] = []
        idx_map: dict[str, list[set[int]]] = {}

        # Use Morgan bit info to enumerate environments
        bitInfo = {}
        rdMolDescriptors.GetMorganFingerprint(
            mol, radius, useCounts=True, useFeatures=False, bitInfo=bitInfo)

        for _, envs in bitInfo.items():
            for center_atom, r in envs:
                if r < min_radius or r > radius:
                    continue
                if r == 0:
                    atoms = {center_atom}
                    bonds = []
                else:
                    bonds = Chem.FindAtomEnvironmentOfRadiusN(
                        mol, r, center_atom)
                    atoms = set([center_atom])
                    for bidx in bonds:
                        b = mol.GetBondWithIdx(bidx)
                        atoms.add(b.GetBeginAtomIdx())
                        atoms.add(b.GetEndAtomIdx())

                smi = Chem.MolFragmentToSmiles(
                    mol,
                    atomsToUse=sorted(atoms),
                    bondsToUse=bonds if bonds else None,
                    rootedAtAtom=(center_atom if root_central_atom else -1),
                    isomericSmiles=True,
                    canonical=True
                )
                shingling.append(smi)
                if get_atom_indices:
                    idx_map.setdefault(smi, []).append(set(atoms))

        if rings:
            ring_info = mol.GetRingInfo()
            for ring_atoms in ring_info.AtomRings():
                atom_set = set(ring_atoms)
                # collect bonds that are in ring and between ring atoms
                ring_bonds = []
                for bond in mol.GetBonds():
                    a = bond.GetBeginAtomIdx()
                    b = bond.GetEndAtomIdx()
                    if a in atom_set and b in atom_set and bond.IsInRing():
                        ring_bonds.append(bond.GetIdx())
                smi = Chem.MolFragmentToSmiles(
                    mol,
                    atomsToUse=sorted(atom_set),
                    bondsToUse=ring_bonds if ring_bonds else None,
                    rootedAtAtom=-1,
                    isomericSmiles=True,
                    canonical=True
                )
                shingling.append(smi)
                if get_atom_indices:
                    idx_map.setdefault(smi, []).append(set(atom_set))

        if get_atom_indices:
            return shingling, idx_map
        return shingling

    @staticmethod
    def internal_encode(in_smiles: str, radius: int = 3, min_radius: int = 0, rings: bool = True, get_atom_indices: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False):
        '''Creates an drfp array from a reaction SMILES string.
        Arguments:
            in_smiles: A valid reaction SMILES string
            radius: The drfp radius (a radius of 3 corresponds to drfp6)
            min_radius: The minimum radius that is used to extract n-grams
            rings: Whether or not to include rings in the shingling
        Returns:
            A tuple with two arrays, the first containing the drfp hash values, the second the substructure SMILES
        '''
        import numpy as np
        from rdkit import Chem

        if not isinstance(in_smiles, str):
            raise ValueError("in_smiles must be a reaction SMILES string")

        # Split reaction into reactants and products; allow presence/absence of reagents section
        # Format: reactants>reagents>products or reactants>>products
        parts = in_smiles.split(">")
        if len(parts) == 3:
            reactants_smi, _, products_smi = parts
        elif len(parts) == 2:  # tolerate "reactants>>products"
            reactants_smi, products_smi = parts[0], parts[1]
        elif ">>" in in_smiles:
            reactants_smi, products_smi = in_smiles.split(">>")
        else:
            # If not a reaction, treat as single molecule reaction to empty
            reactants_smi, products_smi = in_smiles, ""

        reactant_mols = [Chem.MolFromSmiles(s)
                         for s in reactants_smi.split(".") if s]
        product_mols = [Chem.MolFromSmiles(s)
                        for s in products_smi.split(".") if s]

        # Create shinglings
        def get_shingles(mol_list, with_indices):
            shingles_all = []
            idx_maps_all = []
            for m in mol_list:
                if with_indices:
                    sh, idx_map = DRFPUtil.shingling_from_mol(
                        m,
                        radius=radius,
                        rings=rings,
                        min_radius=min_radius,
                        get_atom_indices=True,
                        root_central_atom=root_central_atom,
                        include_hydrogens=include_hydrogens
                    )
                    idx_maps_all.append(idx_map)
                else:
                    sh = DRFPUtil.shingling_from_mol(
                        m,
                        radius=radius,
                        rings=rings,
                        min_radius=min_radius,
                        get_atom_indices=False,
                        root_central_atom=root_central_atom,
                        include_hydrogens=include_hydrogens
                    )
                shingles_all.extend(sh)
            return shingles_all, idx_maps_all

        react_sh, react_idx_maps = get_shingles(
            reactant_mols, get_atom_indices)
        prod_sh, prod_idx_maps = get_shingles(product_mols, get_atom_indices)

        react_set = set(react_sh)
        prod_set = set(prod_sh)
        # Differential set (symmetric difference)
        diff = sorted((react_set - prod_set) | (prod_set - react_set))

        hash_values = DRFPUtil.hash(diff)

        if get_atom_indices:
            mapping = {
                "reactants": react_idx_maps,
                "products": prod_idx_maps
            }
            return hash_values, np.array(diff, dtype=object), mapping
        else:
            return hash_values, np.array(diff, dtype=object)

    @staticmethod
    def hash(shingling: list[str]):
        '''Directly hash all the SMILES in a shingling to a 32-bit integer.
        Arguments:
            shingling: A list of n-grams
        Returns:
            A list of hashed n-grams
        '''
        import numpy as np
        import hashlib
        if not shingling:
            return np.array([], dtype=np.uint32)
        out = np.empty(len(shingling), dtype=np.uint32)
        for i, s in enumerate(shingling):
            if not isinstance(s, str):
                s = str(s)
            h = hashlib.sha1(s.encode('utf-8')).digest()
            out[i] = np.frombuffer(h[:4], dtype=np.uint32)[0]
        return out

    @staticmethod
    def fold(hash_values, length: int = 2048):
        '''Folds the hash values to a binary vector of a given length.
        Arguments:
            hash_value: An array containing the hash values
            length: The length of the folded fingerprint
        Returns:
            A tuple containing the folded fingerprint and the indices of the on bits
        '''
        import numpy as np
        if length <= 0:
            raise ValueError("length must be positive")
        if hash_values is None or len(hash_values) == 0:
            return np.zeros(length, dtype=np.uint8), np.array([], dtype=np.int32)
        idx = (hash_values % length).astype(np.int64)
        on_idx = np.unique(idx)
        fp = np.zeros(length, dtype=np.uint8)
        fp[on_idx] = 1
        return fp, on_idx.astype(np.int32)

    @staticmethod
    def encode(X, n_folded_length: int = 2048, min_radius: int = 0, radius: int = 3, rings: bool = True, mapping: bool = False, atom_index_mapping: bool = False, root_central_atom: bool = True, include_hydrogens: bool = False, show_progress_bar: bool = False):
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
        import numpy as np

        # Normalize input to iterable
        if isinstance(X, str):
            smiles_list = [X]
        else:
            smiles_list = list(X)

        fps: list[np.ndarray] = []
        feature_map: dict[int, set[str]] = {}
        atom_maps_all: list = []

        use_tqdm = False
        if show_progress_bar:
            try:
                from tqdm import tqdm  # type: ignore
                iterator = tqdm(smiles_list)
                use_tqdm = True
            except Exception:
                iterator = smiles_list
        else:
            iterator = smiles_list

        for rxn in iterator:
            if atom_index_mapping:
                hashed, shingles, atom_map = DRFPUtil.internal_encode(
                    rxn,
                    radius=radius,
                    min_radius=min_radius,
                    rings=rings,
                    get_atom_indices=True,
                    root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
            else:
                hashed, shingles = DRFPUtil.internal_encode(
                    rxn,
                    radius=radius,
                    min_radius=min_radius,
                    rings=rings,
                    get_atom_indices=False,
                    root_central_atom=root_central_atom,
                    include_hydrogens=include_hydrogens
                )
            fp, on_idx = DRFPUtil.fold(hashed, n_folded_length)
            fps.append(fp)

            if mapping:
                # Map folded index to shingles that hit it
                for s, h in zip(shingles, hashed):
                    idx = int(h % n_folded_length)
                    feature_map.setdefault(idx, set()).add(s)

            if atom_index_mapping:
                atom_maps_all.append(atom_map)

        # Return priority: atom_index_mapping result takes precedence (per type annotation)
        if atom_index_mapping:
            return atom_maps_all
        if mapping:
            return fps, feature_map
        return fps
