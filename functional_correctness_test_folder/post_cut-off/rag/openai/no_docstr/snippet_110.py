
import json
import os
from pathlib import Path
from typing import Dict, Optional


class Hubbie:
    '''Hubbie is a Huggingface hub manager for Chonkie.
    Methods:
        get_recipe(recipe_name: str, lang: Optional[str] = 'en') -> Optional[Dict]:
            Get a recipe from the hub.
        get_recipe_schema() -> Dict:
            Get the current recipe schema from the hub.
    '''

    # Repository where the schema and recipes live
    _REPO_ID = "chonkie/recipes"
    _SCHEMA_FILE = "recipe_schema.json"

    def __init__(self) -> None:
        '''Initialize Hubbie.'''
        self._import_dependencies()
        self.schema = self.get_recipe_schema()

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            from huggingface_hub import hf_hub_download
            from jsonschema import validate as jsonschema_validate
        except Exception as exc:
            raise ImportError(
                "Hubbie requires 'huggingface_hub' and 'jsonschema' packages. "
                f"Original error: {exc}"
            ) from exc
        self.hf_hub_download = hf_hub_download
        self.jsonschema_validate = jsonschema_validate

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        try:
            import huggingface_hub  # noqa: F401
            import jsonschema  # noqa: F401
            return True
        except Exception:
            return False

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        try:
            local_path = self.hf_hub_download(
                repo_id=self._REPO_ID,
                filename=self._SCHEMA_FILE,
                repo_type="dataset",
            )
        except Exception as exc:
            raise ValueError(
                f"Could not download recipe schema from hub: {exc}"
            ) from exc

        try:
            with open(local_path, "r", encoding="utf-8") as f:
                schema = json.load(f)
        except Exception as exc:
            raise ValueError(
                f"Could not load recipe schema JSON: {exc}"
            ) from exc

        return schema

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        try:
            self.jsonschema_validate(instance=recipe, schema=self.schema)
            return True
        except Exception as exc:
            raise ValueError(f"Recipe validation failed: {exc}") from exc

    def get_recipe(
        self,
        recipe_name: str,
        lang: Optional[str] = "en",
    ) -> Optional[Dict]:
        '''Get a recipe from the hub.
        Args:
            recipe_name (str): The name of the recipe to get.
            lang (Optional[str]): The language of the recipe to get.
        Returns:
            Optional[Dict]: The recipe.
        Raises:
            ValueError: If the recipe is not found.
            ValueError: If the recipe is invalid.
        '''
        if not recipe_name:
            raise ValueError("recipe_name must be provided")

        # Build the expected filename
        filename = f"{recipe_name}_{lang}.json"

        try:
            local_path = self.hf_hub_download(
                repo_id=self._REPO_ID,
                filename=filename,
                repo_type="dataset",
            )
        except Exception as exc:
            raise ValueError(
                f"Could not download recipe '{recipe_name}' (lang={lang}) from hub: {exc}"
            ) from exc

        try:
            with open(local_path, "r", encoding="utf-8") as f:
                recipe = json.load(f)
        except Exception as exc:
            raise ValueError(
                f"Could not load recipe JSON for '{recipe_name}': {exc}"
            ) from exc

        # Validate the recipe
        self._validate_recipe(recipe)

        return recipe
