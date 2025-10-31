
import os
from pathlib import Path


class Config:
    """Provide tool to manage configuration."""

    def validate(self, config):
        """
        Validate the configuration object.

        Parameters
        ----------
        config : dict
            Configuration dictionary that must contain a 'template' key.

        Raises
        ------
        TypeError
            If `config` is not a dictionary or the template value is not a string.
        KeyError
            If the 'template' key is missing.
        FileNotFoundError
            If the template file does not exist.
        """
        if not isinstance(config, dict):
            raise TypeError("config must be a dictionary")

        if "template" not in config:
            raise KeyError("config missing required 'template' key")

        template = config["template"]
        if not isinstance(template, str):
            raise TypeError("'template' value must be a string")

        # Resolve the path to an absolute path
        template_path = Path(template).expanduser().resolve()
        if not template_path.is_file():
            raise FileNotFoundError(
                f"Template file '{template_path}' does not exist")

        # Store the resolved path back into the config for consistency
        config["template"] = str(template_path)

        return True

    def get_template_from_config(self, config):
        """
        Retrieve the template path from the configuration object.

        Parameters
        ----------
        config : dict
            Configuration dictionary that must contain a 'template' key.

        Returns
        -------
        str
            Absolute path to the template file.

        Raises
        ------
        Exception
            Propagated from :meth:`validate` if validation fails.
        """
        self.validate(config)
        return config["template"]
