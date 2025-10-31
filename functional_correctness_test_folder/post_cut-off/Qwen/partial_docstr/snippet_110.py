
from typing import Optional, Dict
import requests


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
        self._check_dependencies()
        self.schema = self.get_recipe_schema()

    def _import_dependencies(self) -> None:
        try:
            import json
            import requests
        except ImportError as e:
            raise ImportError(f"Missing dependency: {e}")

    def _check_dependencies(self) -> Optional[bool]:
        try:
            import json
            import requests
            return True
        except ImportError:
            return False

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        response = requests.get(
            "https://huggingface.co/api/models?filter=recipe-schema")
        response.raise_for_status()
        return response.json()

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        from jsonschema import validate, ValidationError
        try:
            validate(instance=recipe, schema=self.schema)
            return True
        except ValidationError:
            return False

    def get_recipe(self, recipe_name: str, lang: Optional[str] = 'en', path: Optional[str] = None) -> Optional[Dict]:
        '''Get a recipe from the hub.
        Args:
            recipe_name (str): The name of the recipe to get.
            lang (Optional[str]): The language of the recipe to get.
            path (Optional[str]): Optionally, provide the path to the recipe.
        Returns:
            Optional[Dict]: The recipe.
        Raises:
            ValueError: If the recipe is not found.
            ValueError: If neither (recipe_name, lang) nor path are provided.
            ValueError: If the recipe is invalid.
        '''
        if not (recipe_name and lang) and not path:
            raise ValueError(
                "Either (recipe_name, lang) or path must be provided.")

        if path:
            try:
                with open(path, 'r') as file:
                    recipe = file.read()
            except FileNotFoundError:
                raise ValueError(f"Recipe not found at path: {path}")
        else:
            response = requests.get(
                f"https://huggingface.co/api/models/{recipe_name}?lang={lang}")
            if response.status_code == 404:
                raise ValueError(
                    f"Recipe '{recipe_name}' not found for language '{lang}'.")
            response.raise_for_status()
            recipe = response.json()

        if not self._validate_recipe(recipe):
            raise ValueError("The recipe is invalid.")

        return recipe
