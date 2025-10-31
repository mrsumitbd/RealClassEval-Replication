
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
        self._import_dependencies()
        self._check_dependencies()
        self.schema_url = "https://huggingface.co/api/models"
        self.recipe_url = "https://huggingface.co/api/datasets"

    def _import_dependencies(self) -> None:
        try:
            import requests
        except ImportError:
            raise ImportError(
                "The 'requests' library is required for Hubbie to function.")

    def _check_dependencies(self) -> Optional[bool]:
        try:
            import requests
            return True
        except ImportError:
            return False

    def get_recipe_schema(self) -> Dict:
        response = requests.get(self.schema_url)
        if response.status_code == 200:
            return response.json()
        return {}

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        schema = self.get_recipe_schema()
        if not schema:
            return False
        # Simple validation example, assuming schema has a 'required' key
        required_fields = schema.get('required', [])
        return all(field in recipe for field in required_fields)

    def get_recipe(self, recipe_name: str, lang: Optional[str] = 'en') -> Optional[Dict]:
        response = requests.get(f"{self.recipe_url}/{recipe_name}")
        if response.status_code == 200:
            recipe = response.json()
            if self._validate_recipe(recipe):
                return recipe
        return None
