
from typing import Dict, Optional
import importlib
from pathlib import Path
import json
from huggingface_hub import hf_hub_download, HfApi
import jsonschema


class Hubbie:
    '''Hubbie is a Huggingface hub manager for Chonkie.
    Methods:
        get_recipe(recipe_name: str, lang: Optional[str] = 'en') -> Optional[Dict]:
            Get a recipe from the hub.
        get_recipe_schema() -> Dict:
            Get the current recipe schema from the hub.
    '''

    def __init__(self) -> None:
        '''Initialize Hubbie.'''
        self._import_dependencies()
        self._api = HfApi()
        self._schema = None

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            global hf_hub_download, HfApi, jsonschema
            from huggingface_hub import hf_hub_download, HfApi
            import jsonschema
        except ImportError:
            raise ImportError(
                "Required dependencies 'huggingface-hub' and 'jsonschema' not found.")

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        try:
            importlib.import_module('huggingface_hub')
            importlib.import_module('jsonschema')
            return True
        except ImportError:
            return False

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        if self._schema is None:
            schema_path = hf_hub_download(
                repo_id="chonkie/recipes",
                filename="schema.json",
                repo_type="dataset"
            )
            with open(schema_path, 'r') as f:
                self._schema = json.load(f)
        return self._schema

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        schema = self.get_recipe_schema()
        try:
            jsonschema.validate(instance=recipe, schema=schema)
            return True
        except jsonschema.ValidationError:
            return False

    def get_recipe(self, name: Optional[str] = None, lang: Optional[str] = 'en', path: Optional[str] = None) -> Dict:
        '''Get a recipe from the hub.
        Args:
            name (Optional[str]): The name of the recipe to get.
            lang (Optional[str]): The language of the recipe to get.
            path (Optional[str]): Optionally, provide the path to the recipe.
        Returns:
            Optional[Dict]: The recipe.
        Raises:
            ValueError: If the recipe is not found.
            ValueError: If neither (name, lang) nor path are provided.
            ValueError: If the recipe is invalid.
        '''
        if path is None:
            if name is None:
                raise ValueError(
                    "Either (name, lang) or path must be provided.")
            filename = f"{name}_{lang}.json" if lang else f"{name}.json"
            try:
                path = hf_hub_download(
                    repo_id="chonkie/recipes",
                    filename=filename,
                    repo_type="dataset"
                )
            except Exception as e:
                raise ValueError(
                    f"Recipe '{name}' (lang: {lang}) not found.") from e
        try:
            with open(path, 'r') as f:
                recipe = json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to load recipe from {path}.") from e
        if not self._validate_recipe(recipe):
            raise ValueError(f"Recipe at {path} is invalid.")
        return recipe
