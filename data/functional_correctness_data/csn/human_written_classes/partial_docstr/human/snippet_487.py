from openbabel import pybel

class Mapper:
    """Provides functions for mapping atom IDs in the correct way"""

    def __init__(self):
        self.proteinmap = None
        self.ligandmaps = {}
        self.original_structure = None

    def mapid(self, idx, mtype, bsid=None, to='original'):
        if mtype == 'reversed':
            return self.reversed_proteinmap[idx]
        if mtype == 'protein':
            return self.proteinmap[idx]
        elif mtype == 'ligand':
            if to == 'internal':
                return self.ligandmaps[bsid][idx]
            elif to == 'original':
                return self.proteinmap[self.ligandmaps[bsid][idx]]

    def id_to_atom(self, idx):
        """Returns the atom for a given original ligand ID.
        To do this, the ID is mapped to the protein first and then the atom returned.
        """
        mapped_idx = self.mapid(idx, 'reversed')
        return pybel.Atom(self.original_structure.GetAtom(mapped_idx))