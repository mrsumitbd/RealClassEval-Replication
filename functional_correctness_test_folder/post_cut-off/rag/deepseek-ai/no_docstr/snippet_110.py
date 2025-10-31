
from typing import Dict, Optional
import importlib
from pathlib import Path
import json
import requests
from jsonschema import validate, ValidationError


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
        self._schema = None
        self._base_url = "https://huggingface.co/api/recipes"

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            global requests, validate, ValidationError
            requests = importlib.import_module('requests')
            from jsonschema import validate, ValidationError
        except ImportError:
            raise ImportError(
                "Required dependencies 'requests' and 'jsonschema' not found.")

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        try:
            importlib.import_module('requests')
            importlib.import_module('jsonschema')
            return True
        except ImportError:
            return False

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        if self._schema is None:
            schema_url = f"{self._base_url}/schema"
            response = requests.get(schema_url)
            response.raise_for_status()
            self._schema = response.json()
        return self._schema

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        schema = self.get_recipe_schema()
        try:
            validate(instance=recipe, schema=schema)
            return True
        except ValidationError as e:
            raise ValueError(f"Recipe validation failed: {e}")

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
        if path is not None:
            recipe_path = Path(path)
            if not recipe_path.exists():
                raise ValueError(f"Recipe file not found at {path}")
            with open(recipe_path, 'r') as f:
                recipe = json.load(f)
        elif name is not None:
            url = f"{self._base_url}/{name}/{lang}"
            response = requests.get(url)
            if response.status_code == 404:
                raise ValueError(
                    f"Recipe '{name}' with language '{lang}' not found.")
            response.raise_for_status()
            recipe = response.json()
        else:
            raise ValueError("Either (name, lang) or path must be provided.")

        self._validate_recipe(recipe)
        return recipe
