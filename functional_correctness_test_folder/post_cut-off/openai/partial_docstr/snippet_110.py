
import json
import os
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
        '''Initialize Hubbie.'''
        self._import_dependencies()
        if not self._check_dependencies():
            raise RuntimeError(
                "Required dependencies are missing. Install 'huggingface_hub'.")

    def _import_dependencies(self) -> None:
        try:
            from huggingface_hub import hf_hub_download
            self.hf_hub_download = hf_hub_download
        except Exception:
            self.hf_hub_download = None

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        return self.hf_hub_download is not None

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        repo_id = "chonkie/recipes"
        filename = "schema.json"
        try:
            local_path = self.hf_hub_download(
                repo_id=repo_id, filename=filename, force_download=False)
            with open(local_path, "r", encoding="utf-8") as f:
                schema = json.load(f)
            return schema
        except Exception as e:
            raise RuntimeError(f"Could not load schema from hub: {e}")

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        schema = self.get_recipe_schema()
        required = schema.get("required", [])
        missing = [k for k in required if k not in recipe]
        if missing:
            raise ValueError(f"Recipe missing required fields: {missing}")
        return True

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
        if path:
            if not os.path.isfile(path):
                raise ValueError(f"Provided path does not exist: {path}")
            with open(path, "r", encoding="utf-8") as f:
                recipe = json.load(f)
        else:
            if not recipe_name or not lang:
                raise ValueError(
                    "Either path or both recipe_name and lang must be provided.")
            repo_id = "chonkie/recipes"
            filename = f"{recipe_name}_{lang}.json"
            try:
                local_path = self.hf_hub_download(
                    repo_id=repo_id, filename=filename, force_download=False)
                with open(local_path, "r", encoding="utf-8") as f:
                    recipe = json.load(f)
            except Exception as e:
                raise ValueError(
                    f"Could not download recipe '{recipe_name}' in language '{lang}': {e}")

        # Validate recipe
        self._validate_recipe(recipe)
        return recipe
