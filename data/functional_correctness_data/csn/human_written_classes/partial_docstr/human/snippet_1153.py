class Source:
    """
    A `Source` for a concept, collection or scheme.

    """
    citation = None
    'A bibliographic citation for this source.'
    markup = None
    '\n    What kind of markup does the source contain?\n\n    If not `None`, the source should be treated as a certain type of markup.\n    Currently only HTML is allowed.\n    '

    def __init__(self, citation, markup=None):
        self.citation = citation
        if self.is_valid_markup(markup):
            self.markup = markup
        else:
            raise ValueError(f'{markup} is not valid markup.')

    @staticmethod
    def is_valid_markup(markup):
        """
        Check the argument is a valid type of markup.

        :param string markup: The type to be checked.
        """
        return markup in valid_markup