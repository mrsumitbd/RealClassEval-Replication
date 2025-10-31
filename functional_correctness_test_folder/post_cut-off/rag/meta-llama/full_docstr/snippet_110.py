
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
        self.recipe_schema_url = f'{self.hub_url}/chonkie/recipe-schema/main/schema.json'

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            global requests, jsonschema
            import requests
            import jsonschema
        except ImportError as e:
            raise ImportError(
                'Required dependencies not found. Please install requests and jsonschema.') from e

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
        response = requests.get(self.recipe_schema_url)
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
        return None

    def get_recipe(self, recipe_name: str, lang: Optional[str] = 'en') -> Optional[Dict]:
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
        if not recipe_name:
            raise ValueError('Recipe name is required')
        recipe_url = f'{self.hub_url}/chonkie/{recipe_name}/resolve/main/{lang}/recipe.json'
        response = requests.get(recipe_url)
        if response.status_code == 200:
            recipe = response.json()
            if self._validate_recipe(recipe):
                return recipe
            else:
                raise ValueError('Invalid recipe')
        else:
            raise ValueError('Recipe not found')
