from pymatgen.core.structure import Structure
import numpy as np
from pymatgen.core.lattice import Lattice
from pymatgen.phonon.bandstructure import PhononBandStructureSymmLine

class CastepPhonon:
    """Data from CASTEP phonon calculation: seedname.phonon file

    Usually this will be instantiated with the
    :obj:`sumo.io.castep.CastepPhonon.from_file()` method

    """

    def __init__(self, header, qpts, frequencies, weights=None, eigenvectors=None):
        """
        Args:
            header (:obj:`dict`):
                Dict containing key metadata from header file. Positions are in
                fractional coordinates.

                  {nions: NIONS, nbranches: NBRANCHES, nqpts: NQPTS,
                   frequency_unit: 'cm-1',
                   cell: [[ax, ay, az], [bx, by, bz], [cx, cy, cz]],
                   positions: [[a1, b1, c1], [a2, b2, c2], ...],
                   symbols: [el1, el2, ...],
                   masses: [m1, m2, ...]}

            qpts (:obj:`numpy.ndarray`):
                Nx3 array of q-points in fractional coordinates
            frequencies (:obj:`numpy.ndarray`):
                2-D array of frequencies arranged [mode, qpt]. (Frequencies are
                in units of header['frequency_unit']).
            weights (:obj:`numpy.ndarray`, optional):
                1-D array of q-point weights (not used in band structure plot).
            eigenvectors (:obj:`numpy.ndarray`, optional):
                4-D array of phonon eigenvectors arranged
                [mode, qpt, atom, xyz] (not used in band structure plot).

        """
        self.header = header
        self.qpts = qpts
        self.weights = weights
        self.frequencies = frequencies
        self.eigenvectors = eigenvectors
        self.labels = {}

    @classmethod
    def from_file(cls, filename):
        """Create a CastepPhonon object by reading CASTEP .phonon file

        Args:
            filename (:obj:`str`): Input .phonon file

        Returns:
            pymatgen.phonon.bandstructure.PhononBandStructure
        """
        header = read_phonon_header(filename)
        qpts, weights, frequencies, eigenvectors = read_phonon_bands(filename, header)
        return cls(header, qpts, frequencies, weights=weights, eigenvectors=eigenvectors)

    def set_labels_from_file(self, filename):
        """Set dictionary of special-point labels from .cell file comments

        Args:
            filename (:obj:`str`):
                Input .cell file. Special point symbols should be included as
                comments on the lines where those qpts are defined; *kgen* will
                do this automatically when writing high-symmetry paths.

        """
        self.labels = labels_from_cell(filename, phonon=True)

    def get_band_structure(self):
        lattice = Lattice(self.header['cell'])
        structure = Structure(lattice, species=self.header['symbols'], coords=self.header['positions'])
        mass_weights = 1 / np.sqrt(self.header['masses'])
        displacements = self.eigenvectors * mass_weights[np.newaxis, np.newaxis, :, np.newaxis]
        return PhononBandStructureSymmLine(self.qpts, self.frequencies, lattice.reciprocal_lattice, structure=structure, eigendisplacements=displacements, labels_dict=self.labels)