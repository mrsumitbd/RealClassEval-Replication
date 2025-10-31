from pathlib import Path
from pysd.translators.structures.abstract_model import AbstractComponent, AbstractElement, AbstractControlElement, AbstractModel, AbstractSection

class ModelBuilder:
    """
    ModelBuilder allows building a PySD Python model from the
    Abstract Model.

    Parameters
    ----------
    abstract_model: AbstractModel
        The abstract model to build.

    """

    def __init__(self, abstract_model: AbstractModel):
        self.__dict__ = abstract_model.__dict__.copy()
        self.sections = [SectionBuilder(section) for section in abstract_model.sections]
        self.macrospace = {section.name: section for section in self.sections[1:]}

    def build_model(self) -> Path:
        """
        Build the Python model in a file callled as the orginal model
        but with '.py' suffix.

        Returns
        -------
        path: pathlib.Path
            The path to the new PySD model.

        """
        for section in self.sections:
            section.macrospace = self.macrospace
            section.build_section()
        return self.sections[0].path