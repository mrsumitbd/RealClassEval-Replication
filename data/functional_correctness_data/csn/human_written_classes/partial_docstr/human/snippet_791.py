from foyer.smarts import SMARTS

class AtomTypingRulesProvider:
    """A generic rules provider for atomtyping, agnostic of the forcefield.

    Parameters
    ----------
    atomtype_definitions: dict, required
        The smarts definition for the atomtypes
    atomtype_overrides: dict, required
        The overrides for particular atomtypes
    non_element_types: set, required
        The non-element types used for atomtyping
    parser: The chemical grammar parser, default=None
        The parser for the SMARTS strings. If not provided foyer.smarts.SMARTS
        instance will be used.
    """

    def __init__(self, atomtype_definitions, atomtype_overrides, non_element_types, parser=None):
        self.atomtype_definitions = atomtype_definitions
        self.atomtype_overrides = atomtype_overrides
        self.non_element_types = non_element_types
        self.parser = parser or SMARTS(self.non_element_types)

    @classmethod
    def from_foyer_forcefield(cls, ff):
        """Create an instance of the rules provider for a foyer-forcefield."""
        return cls(atomtype_definitions=ff.atomTypeDefinitions, atomtype_overrides=ff.atomTypeOverrides, non_element_types=ff.non_element_types, parser=ff.parser)