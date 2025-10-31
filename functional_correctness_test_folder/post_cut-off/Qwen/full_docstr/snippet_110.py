
from typing import Optional, Dict
import json
import os


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
        self.schema = self.get_recipe_schema()

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            import requests
        except ImportError:
            raise ImportError(
                "The 'requests' library is required for Hubbie to function.")

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        try:
            import requests
            return True
        except ImportError:
            return False

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        # This is a placeholder URL; replace with actual schema URL
        schema_url = "https://huggingface.co/path/to/schema.json"
        response = requests.get(schema_url)
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
        if path:
            if not os.path.exists(path):
                raise ValueError("The provided path does not exist.")
            with open(path, 'r') as file:
                recipe = json.load(file)
        elif name:
            # This is a placeholder URL; replace with actual recipe URL
            recipe_url = f"https://huggingface.co/path/to/{name}_{lang}.json"
            response = requests.get(recipe_url)
            if response.status_code == 404:
                raise ValueError("The recipe was not found.")
            response.raise_for_status()
            recipe = response.json()
        else:
            raise ValueError("Either (name, lang) or path must be provided.")

        if not self._validate_recipe(recipe):
            raise ValueError("The recipe is invalid.")

        return recipe
