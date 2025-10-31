
from typing import Dict, Optional
import requests
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
        self.schema = self.get_recipe_schema()

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            global requests, jsonschema
            import requests
            import jsonschema
        except ImportError as e:
            raise ImportError(
                "Missing required dependencies. Please install 'requests' and 'jsonschema'.") from e

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
        url = "https://huggingface.co/datasets/chonkie/recipes/raw/main/schema.json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("Failed to retrieve the recipe schema.")

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        try:
            jsonschema.validate(instance=recipe, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError:
            return False

    def get_recipe(self, recipe_name: str, lang: Optional[str] = 'en') -> Optional[Dict]:
        '''Get a recipe from the hub.
        Args:
            recipe_name (str): The name of the recipe to get.
            lang (Optional[str]): The language of the recipe to get. Defaults to 'en'.
        Returns:
            Optional[Dict]: The recipe.
        Raises:
            ValueError: If the recipe is not found.
            ValueError: If the recipe is invalid.
        '''
        if not recipe_name:
            raise ValueError("Recipe name is required.")

        url = f"https://huggingface.co/datasets/chonkie/recipes/raw/main/recipes/{lang}/{recipe_name}.json"
        response = requests.get(url)
        if response.status_code == 200:
            recipe = response.json()
            if self._validate_recipe(recipe):
                return recipe
            else:
                raise ValueError("The retrieved recipe is invalid.")
        else:
            raise ValueError("Recipe not found.")
