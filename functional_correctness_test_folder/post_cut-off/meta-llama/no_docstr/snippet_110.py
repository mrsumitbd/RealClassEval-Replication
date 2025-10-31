
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
        self._import_dependencies()
        if not self._check_dependencies():
            raise ImportError("Missing dependencies")

    def _import_dependencies(self) -> None:
        global requests
        global jsonschema
        try:
            import requests
            import jsonschema
        except ImportError as e:
            raise ImportError("Missing dependencies") from e

    def _check_dependencies(self) -> Optional[bool]:
        try:
            import requests
            import jsonschema
            return True
        except ImportError:
            return False

    def get_recipe_schema(self) -> Dict:
        response = requests.get(
            'https://huggingface.co/api/models/chonkie/recipes/main/schema')
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Failed to retrieve recipe schema. Status code: {response.status_code}")

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        schema = self.get_recipe_schema()
        try:
            jsonschema.validate(instance=recipe, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError:
            return False

    def get_recipe(self, recipe_name: str, lang: Optional[str] = 'en') -> Optional[Dict]:
        response = requests.get(
            f'https://huggingface.co/api/models/chonkie/recipes/main/{lang}/{recipe_name}')
        if response.status_code == 200:
            recipe = response.json()
            if self._validate_recipe(recipe):
                return recipe
            else:
                return None
        else:
            return None
