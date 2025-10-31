
import re
from typing import Dict


class PromptCompiler:
    """
    A simple prompt compiler that reads a prompt file and substitutes
    placeholders with provided parameters.
    """

    def __init__(self):
        # No initialization needed for now
        pass

    def compile(self, prompt_file: str, params: Dict[str, str]) -> str:
        """
        Read the prompt file, substitute parameters, and return the final prompt string.

        Parameters
        ----------
        prompt_file : str
            Path to the prompt template file.
        params : Dict[str, str]
            Mapping of placeholder names to their replacement values.

        Returns
        -------
        str
            The compiled prompt with all placeholders replaced.
        """
        try:
            with open(prompt_file, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Prompt file not found: {prompt_file}") from e

        return self._substitute_parameters(content, params)

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        """
        Replace placeholders in the content with values from params.

        Supported placeholder formats:
            - {{placeholder}}
            - ${placeholder}
            - ${placeholder:default}  (default value used if key missing)

        Parameters
        ----------
        content : str
            The template content.
        params : Dict[str, str]
            Mapping of placeholder names to their replacement values.

        Returns
        -------
        str
            The content with placeholders replaced.
        """
        # Pattern for {{placeholder}} and ${placeholder} with optional default
        pattern = re.compile(r"""
            (?:\{\{(?P<key1>\w+)\}\}) |          # {{key}}
            (?:\${(?P<key2>\w+)(?::(?P<default>[^}]*))?})   # ${key} or ${key:default}
        """, re.VERBOSE)

        def replacer(match):
            key = match.group("key1") or match.group("key2")
            default = match.group("default")
            if key in params:
                return str(params[key])
            if default is not None:
                return default
            # If key not found and no default, leave placeholder unchanged
            return match.group(0)

        return pattern.sub(replacer, content)
