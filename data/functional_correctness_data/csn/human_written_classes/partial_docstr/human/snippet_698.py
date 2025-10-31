from monty.io import zopen
from pymatgen.core.lattice import Lattice
from pymatgen.core.structure import Structure
import re

class QuestaalSite:
    """Structure information: Questaal site.ext file

    Usually this will be instantiated with the
    :obj:`~sumo.io.questaal.QuestaalSite.from_file()` method.

    """

    def __init__(self, nbas, vn=3.0, io=15, alat=1.0, xpos=True, read='fast', sites=None, plat=(1, 0, 0, 0, 1, 0, 0, 0, 1)):
        sites = sites or []
        if nbas != len(sites):
            raise AssertionError()
        if len(plat) != 9:
            raise AssertionError()
        if read != 'fast':
            raise Exception("Algebraic expressions not supported, use 'fast'")
        if io != 15:
            raise Exception('Only site.ext format 15 supported at present')
        self.nbas, self.vn, self.io, self.alat = (nbas, vn, io, alat)
        self.xpos, self.read, self.sites, self.plat = (xpos, read, sites, plat)
        is_empty = re.compile('E\\d*$')
        empty_sites = [site for site in sites if is_empty.match(site['species']) is not None]
        self.nbas_empty = len(empty_sites)

    @property
    def structure(self):
        lattice = Lattice(self.plat)
        lattice = Lattice(lattice.matrix * self.alat * _bohr_to_angstrom)
        if self.xpos:
            species_coords = [(site['species'], site['pos']) for site in self.sites]
            species, coords = zip(*species_coords)
            return Structure(lattice, species, coords, coords_are_cartesian=False)
        else:
            species_coords = [(site['species'], [x * self.alat * _bohr_to_angstrom for x in site['pos']]) for site in self.sites]
            species, coords = zip(*species_coords)
            return Structure(lattice, species, coords, coords_are_cartesian=True)

    @classmethod
    def from_file(cls, filename):
        with zopen(filename, 'rt') as f:
            lines = f.readlines()
        header = lines[0]
        sites = [line for line in lines if line[0] not in '#%']
        header_items = header.strip().split()
        if header_items[0] != '%' or header_items[1] != 'site-data':
            raise AssertionError()
        xpos = True if 'xpos' in header_items else False
        read = 'fast' if 'fast' in header_items else False
        header_clean = ' '.join((x for x in header_items if x not in ('%', 'site-data', 'xpos', 'fast')))
        tags = re.findall('(\\w+)\\s*=', header_clean)
        tag_data = re.split('\\s*\\w+\\s*=\\s*', header_clean)[1:]
        tag_dict = dict(zip(tags, tag_data))
        vn = float(tag_dict['vn']) if 'vn' in tag_dict else 3.0
        io = int(tag_dict['io']) if 'io' in tag_dict else 15.0
        nbas = int(tag_dict['nbas']) if 'nbas' in tag_dict else 15.0
        alat = float(tag_dict['alat']) if 'alat' in tag_dict else 1.0
        plat = [float(x) for x in tag_dict['plat'].split()] if 'plat' in tag_dict else [1, 0, 0, 0, 1, 0, 0, 0, 1]
        sites = [{'species': site.split()[0], 'pos': [float(x) for x in site.split()[1:4]]} for site in sites]
        return cls(nbas, vn=vn, io=io, alat=alat, xpos=xpos, read=read, sites=sites, plat=plat)