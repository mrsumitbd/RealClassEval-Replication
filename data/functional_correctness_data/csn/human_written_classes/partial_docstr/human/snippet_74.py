from pyinstrument.session import Session

class Renderer:
    """
    Abstract base class for renderers.
    """
    output_file_extension: str = 'txt'
    '\n    Renderer output file extension without dot prefix. The default value is `txt`\n    '
    output_is_binary: bool = False
    '\n    Whether the output of this renderer is binary data. The default value is `False`.\n    '

    def __init__(self):
        pass

    def render(self, session: Session) -> str:
        """
        Return a string that contains the rendered form of `frame`.
        """
        raise NotImplementedError()

    class MisconfigurationError(Exception):
        pass