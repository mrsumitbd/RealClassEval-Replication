
from typing import Dict, Optional
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

    HUB_URL = "https://huggingface.co/api/models"
    SCHEMA_URL = "https://huggingface.co/api/models/chonkie/recipe-schema/raw"

    def __init__(self) -> None:
        '''Initialize Hubbie.'''
        self._import_dependencies()
        self.schema = self.get_recipe_schema()

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            import requests
            import jsonschema
        except ImportError as e:
            raise ImportError(f"Missing dependency: {e.name}")

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        try:
            import requests
            import jsonschema
            return True
        except ImportError:
            return False

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        response = requests.get(self.SCHEMA_URL)
        response.raise_for_status()
        return response.json()

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        try:
            validate(instance=recipe, schema=self.schema)
            return True
        except ValidationError as e:
            print(f"Validation error: {e}")
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
            ValueError: If neither (name, lang) nor path are provided.
            ValueError: If the recipe is invalid.
        '''
        if not path and not (recipe_name and lang):
            raise ValueError("Either (name, lang) or path must be provided.")

        if path:
            try:
                with open(path, 'r') as file:
                    recipe = json.load(file)
            except FileNotFoundError:
                raise ValueError(f"Recipe file not found at {path}.")
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON in recipe file at {path}.")
        else:
            response = requests.get(f"{self.HUB_URL}/{recipe_name}/{lang}/raw")
            if response.status_code == 404:
                raise ValueError(
                    f"Recipe '{recipe_name}' in language '{lang}' not found.")
            response.raise_for_status()
            recipe = response.json()

        if not self._validate_recipe(recipe):
            raise ValueError("The recipe is invalid.")

        return recipe
