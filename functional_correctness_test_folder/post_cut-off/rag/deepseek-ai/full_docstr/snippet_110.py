
from typing import Dict, Optional
import importlib
import json
from pathlib import Path
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

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            global validate, ValidationError
            from jsonschema import validate, ValidationError
        except ImportError:
            raise ImportError(
                "jsonschema is required for Hubbie. Please install it with `pip install jsonschema`.")

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        try:
            importlib.import_module('jsonschema')
            return True
        except ImportError:
            return False

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        if self._schema is None:
            schema_path = Path(__file__).parent / \
                'schemas' / 'recipe_schema.json'
            if not schema_path.exists():
                raise FileNotFoundError(
                    f"Recipe schema not found at {schema_path}")
            with open(schema_path, 'r') as f:
                self._schema = json.load(f)
        return self._schema

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        schema = self.get_recipe_schema()
        try:
            validate(instance=recipe, schema=schema)
            return True
        except ValidationError as e:
            raise ValueError(f"Recipe validation failed: {e.message}")

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
            recipe_path = Path(__file__).parent / \
                'recipes' / lang / f"{name}.json"
        else:
            recipe_path = Path(path)

        if not recipe_path.exists():
            raise ValueError(f"Recipe not found at {recipe_path}")

        with open(recipe_path, 'r') as f:
            recipe = json.load(f)

        self._validate_recipe(recipe)
        return recipe
