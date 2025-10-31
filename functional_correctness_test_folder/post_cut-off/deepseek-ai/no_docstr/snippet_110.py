
from typing import Dict, Optional
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
        self._base_url = "https://huggingface.co/api"
        self._dependencies_loaded = False
        self._import_dependencies()
        self._check_dependencies()

    def _import_dependencies(self) -> None:
        try:
            global requests
            import requests
            self._dependencies_loaded = True
        except ImportError:
            self._dependencies_loaded = False

    def _check_dependencies(self) -> Optional[bool]:
        return self._dependencies_loaded

    def get_recipe(self, recipe_name: str, lang: Optional[str] = 'en') -> Optional[Dict]:
        if not self._dependencies_loaded:
            return None
        url = f"{self._base_url}/recipes/{recipe_name}"
        params = {'lang': lang} if lang else None
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            recipe = response.json()
            if self._validate_recipe(recipe):
                return recipe
            return None
        except requests.exceptions.RequestException:
            return None

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        schema = self.get_recipe_schema()
        if not schema:
            return False
        try:
            for key in schema['required']:
                if key not in recipe:
                    return False
            return True
        except KeyError:
            return False

    def get_recipe_schema(self) -> Dict:
        if not self._dependencies_loaded:
            return {}
        url = f"{self._base_url}/recipes/schema"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return {}
