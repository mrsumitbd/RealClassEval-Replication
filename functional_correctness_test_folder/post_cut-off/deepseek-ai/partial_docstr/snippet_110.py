
from typing import Dict, Optional
import requests
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError


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
        '''Import required dependencies.'''
        try:
            global requests, json, validate, ValidationError
            import requests
            import json
            from jsonschema import validate
            from jsonschema.exceptions import ValidationError
        except ImportError as e:
            raise ImportError(f"Missing required dependencies: {e}")

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        try:
            import requests
            import json
            from jsonschema import validate
            from jsonschema.exceptions import ValidationError
            return True
        except ImportError:
            return False

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        if self._schema is None:
            response = requests.get(f"{self._base_url}/schema")
            if response.status_code == 200:
                self._schema = response.json()
            else:
                raise ValueError("Failed to fetch recipe schema.")
        return self._schema

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        schema = self.get_recipe_schema()
        try:
            validate(instance=recipe, schema=schema)
            return True
        except ValidationError:
            return False

    def get_recipe(self, name: Optional[str] = None, lang: Optional[str] = 'en', path: Optional[str] = None) -> Optional[Dict]:
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
            path = f"{name}/{lang}"

        response = requests.get(f"{self._base_url}/{path}")
        if response.status_code != 200:
            raise ValueError(f"Recipe not found: {path}")

        recipe = response.json()
        if not self._validate_recipe(recipe):
            raise ValueError(f"Invalid recipe: {path}")

        return recipe
