
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
        self.hub_url = 'https://huggingface.co'

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            global requests, jsonschema
            import requests
            import jsonschema
        except ImportError as e:
            raise ImportError(
                'Required dependencies not available. Please install requests and jsonschema.') from e

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
        response = requests.get(
            f'{self.hub_url}/chonkie/recipe-schema/main/schema.json')
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError('Failed to retrieve recipe schema')

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        schema = self.get_recipe_schema()
        try:
            jsonschema.validate(instance=recipe, schema=schema)
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
        response = requests.get(
            f'{self.hub_url}/chonkie/{recipe_name}/resolve/main/{lang}/recipe.json')
        if response.status_code == 200:
            recipe = response.json()
            if self._validate_recipe(recipe):
                return recipe
            else:
                raise ValueError('Invalid recipe')
        else:
            raise ValueError('Recipe not found')
