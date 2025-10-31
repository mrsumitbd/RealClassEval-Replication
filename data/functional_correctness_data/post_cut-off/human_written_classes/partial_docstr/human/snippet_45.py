import json
from typing import Dict, List, Optional, Union, Any
from pathlib import Path

class TemplateManager:
    """Manages templates with cascading override support"""

    def __init__(self, custom_template_dir: Optional[str]=None):
        self.default_dir = Path(__file__).parent.parent / 'prompts' / 'defaults'
        self.custom_dir = Path(custom_template_dir) if custom_template_dir else None
        self.templates = {}
        self.fragments = {}
        self._load_from_directory(self.default_dir)
        if self.custom_dir and self.custom_dir.exists():
            self._load_from_directory(self.custom_dir)

    def _load_from_directory(self, directory: Path) -> None:
        """Load all templates and fragments from a directory"""
        if not directory.exists():
            return
        for txt_file in directory.glob('*.txt'):
            template_name = txt_file.stem
            with open(txt_file, 'r') as f:
                self.templates[template_name] = f.read()
        fragments_file = directory / 'fragments.json'
        if fragments_file.exists():
            with open(fragments_file, 'r') as f:
                loaded_fragments = json.load(f)
                self.fragments.update(loaded_fragments)

    def get_template(self, name: str) -> str:
        """Get a template by name"""
        if name not in self.templates:
            raise ValueError(f"Template '{name}' not found")
        return self.templates[name]

    def get_fragment(self, name: str, **kwargs) -> str:
        """Get and format a fragment"""
        if name not in self.fragments:
            return f'[Missing fragment: {name}]'
        try:
            return self.fragments[name].format(**kwargs)
        except KeyError as e:
            return f'[Fragment formatting error: {e}]'

    def add_template(self, template_name: str, template: str) -> None:
        """Add or update a template"""
        self.templates[template_name] = template

    def add_fragment(self, fragment_name: str, fragment: str) -> None:
        """Add or update a fragment"""
        self.fragments[fragment_name] = fragment