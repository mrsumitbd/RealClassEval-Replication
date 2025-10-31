from sphinx.errors import ConfigError
import types
import os

class ExplicitOrder:
    """Sorting key for all gallery subsections.

    All subsections folders must be listed, otherwise an exception is raised.
    However, you can add '*' as a placeholder to the list. All not-listed
    subsection folders will be inserted at the given position and no
    exception is raised.

    Parameters
    ----------
    ordered_list : list, tuple, or :term:`python:generator`
        Hold the paths of each galleries' subsections.

    Raises
    ------
    ValueError
        Wrong input type or Subgallery path missing.
    """

    def __init__(self, ordered_list):
        if not isinstance(ordered_list, (list, tuple, types.GeneratorType)):
            raise ConfigError('ExplicitOrder sorting key takes a list, tuple or Generator, which holdthe paths of each gallery subfolder')
        self.ordered_list = ['*' if path == '*' else os.path.normpath(path) for path in ordered_list]
        try:
            i = ordered_list.index('*')
            self.has_wildcard = True
            self.ordered_list_start = self.ordered_list[:i]
            self.ordered_list_end = self.ordered_list[i + 1:]
        except ValueError:
            self.has_wildcard = False
            self.ordered_list_start = []
            self.ordered_list_end = self.ordered_list

    def __call__(self, item):
        """
        Return an integer suited for ordering the items.

        If the ordered_list contains a wildcard "*", items before "*" will return
        negative numbers, items after "*" will have positive numbers, and
        not-listed items will return 0.

        If there is no wildcard, all items with return positive numbers, and
        not-listed items will raise a ConfigError.
        """
        if item in self.ordered_list_start:
            return self.ordered_list_start.index(item) - len(self.ordered_list_start)
        elif item in self.ordered_list_end:
            return self.ordered_list_end.index(item) + 1
        elif self.has_wildcard:
            return 0
        else:
            raise ConfigError("The subsection folder {!r} was not found in the 'subsection_order' config. If you use an explicit 'subsection_order', you must specify all subsection folders or add '*' as a wildcard to collect all not-listed subsection folders.".format(item))

    def __repr__(self):
        return f'<{self.__class__.__name__} : {self.ordered_list}>'