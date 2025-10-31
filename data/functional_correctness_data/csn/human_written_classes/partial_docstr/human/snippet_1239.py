from pylatexenc.latex2text import LatexNodes2Text
import re

class Latex:
    """A class for handling LaTeX text content."""

    def __init__(self, tex: str) -> None:
        self.tex = tex

    def to_text(self) -> str:
        """Convert LaTeX to text."""
        text = LatexNodes2Text().latex_to_text(self.tex.strip())
        return re.sub(' +', ' ', text)