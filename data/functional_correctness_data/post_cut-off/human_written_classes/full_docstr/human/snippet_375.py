from tests.data import DIPOLE_GRO, DIPOLE_ITP
import MDAnalysis as mda
from maicos import DielectricPlanar

class DielectricPlanarBenchmark:
    """Benchmark the DielectricPlanar class."""

    def setup(self):
        """Setup the analysis objects."""
        self.dipole1 = mda.Universe(DIPOLE_ITP, DIPOLE_GRO, topology_format='itp').atoms
        self.dielectric = DielectricPlanar(self.dipole1)
        self.dielectric._prepare()

    def time_single_dielectric_planar(self):
        """Benchmark of a complete run over a single frame."""
        self.dielectric.run()