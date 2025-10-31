
import importlib
from typing import Dict, Optional


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

    def _import_dependencies(self) -> None:
        self.huggingface_hub = importlib.import_module('huggingface_hub')

    def _check_dependencies(self) -> Optional[bool]:
        if not hasattr(self, 'huggingface_hub'):
            raise ImportError(
                "huggingface_hub is not installed. Please install it using 'pip install huggingface-hub'")
        return True

    def get_recipe_schema(self) -> Dict:
        schema = self.huggingface_hub.hf_hub_download(
            repo_id='chonkie/recipe-schema',
            filename='schema.json',
            repo_type='dataset'
        )
        with open(schema, 'r') as f:
            return json.load(f)

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        schema = self.get_recipe_schema()
        try:
            jsonschema.validate(instance=recipe, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            print(f"Recipe validation failed: {e}")
            return False

    def get_recipe(self, recipe_name: str, lang: Optional[str] = 'en') -> Optional[Dict]:
        recipe = self.huggingface_hub.hf_hub_download(
            repo_id=f'chonkie/recipes-{lang}',
            filename=f'{recipe_name}.json',
            repo_type='dataset'
        )
        with open(recipe, 'r') as f:
            recipe_data = json.load(f)
        if self._validate_recipe(recipe_data):
            return recipe_data
        return None
