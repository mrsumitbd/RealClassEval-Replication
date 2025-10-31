
import importlib
import json
from typing import Dict, Optional
from pathlib import Path


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

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        if not self._check_dependencies():
            raise ImportError(
                "Required dependencies for Hubbie are not available. Please install 'huggingface_hub'.")

        global huggingface_hub
        huggingface_hub = importlib.import_module('huggingface_hub')

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        try:
            importlib.import_module('huggingface_hub')
            return True
        except ImportError:
            return False

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        schema_path = huggingface_hub.hf_hub_download(
            repo_id="chonkie/recipe-schema",
            filename="schema.json",
            repo_type="dataset"
        )
        with open(schema_path, 'r') as f:
            return json.load(f)

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        from jsonschema import validate
        schema = self.get_recipe_schema()
        try:
            validate(instance=recipe, schema=schema)
            return True
        except Exception as e:
            raise ValueError(f"Recipe validation failed: {str(e)}")

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
            recipe_path = Path(path)
            if not recipe_path.exists():
                raise ValueError(f"Recipe file not found at path: {path}")
            with open(recipe_path, 'r') as f:
                recipe = json.load(f)
        elif name and lang:
            recipe_path = huggingface_hub.hf_hub_download(
                repo_id=f"chonkie/recipes-{lang}",
                filename=f"{name}.json",
                repo_type="dataset"
            )
            with open(recipe_path, 'r') as f:
                recipe = json.load(f)
        else:
            raise ValueError("Either (name, lang) or path must be provided.")

        if not self._validate_recipe(recipe):
            raise ValueError("Recipe is invalid.")

        return recipe
