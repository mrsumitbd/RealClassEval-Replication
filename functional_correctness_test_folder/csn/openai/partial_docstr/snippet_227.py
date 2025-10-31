
from dataclasses import dataclass


@dataclass
class TemplateFile:
    """Represents a template file with its textual content."""
    content: str = ""

    def save(self, file_name: str) -> None:
        """
        Write the template content to the specified file.

        Parameters
        ----------
        file_name : str
            Path to the file where the content should be written.
        """
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(self.content)

    @classmethod
    def from_file(cls, file_name: str) -> "TemplateFile":
        """
        Read the content of a file and create a TemplateFile instance.

        Parameters
        ----------
        file_name : str
            Path to the file to read.

        Returns
        -------
        TemplateFile
            An instance containing the file's content.
        """
        with open(file_name, "r", encoding="utf-8") as f:
            content = f.read()
        return cls(content=content)
