
import json
import os
from pathlib import Path


class Config:
    '''Provide tool to manage config.'''

    def _load_config(self, config):
        """
        Internal helper that normalises the config input.
        Returns a dictionary representation of the config.
        """
        if isinstance(config, dict):
            return config

        # Accept Path-like objects
        if isinstance(config, (Path, str)):
            path = Path(config)
            if not path.is_file():
                raise ValueError(
                    f"Config file '{path}' does not exist or is not a file.")
            try:
                with path.open('r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Config file '{path}' is not valid JSON: {exc}") from exc
            if not isinstance(data, dict):
                raise ValueError(
                    f"Config file '{path}' must contain a JSON object at the top level.")
            return data

        raise TypeError(
            "Config must be a dict, a Path, or a string path to a JSON file.")

    def validate(self, config):
        '''Validate that the source file is ok.'''
        cfg = self._load_config(config)

        # Basic validation: must contain 'template_path'
        if 'template_path' not in cfg:
            raise ValueError("Config must contain a 'template_path' key.")

        # Validate that the template path is a non-empty string
        template_path = cfg['template_path']
        if not isinstance(template_path, str) or not template_path.strip():
            raise ValueError("'template_path' must be a non-empty string.")

        # Optionally, check that the template file exists
        template_file = Path(template_path)
        if not template_file.is_file():
            raise ValueError(
                f"Template file '{template_file}' does not exist or is not a file.")

        # If all checks pass, return the normalised config
        return cfg

    def get_template_from_config(self, config):
        '''Retrieve a template path from the config object.'''
        cfg = self._load_config(config)
        return cfg['template_path']
