
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Optional

# The class relies on optional external libraries. They are imported lazily
# in `_import_dependencies` to avoid import errors when the class is defined.


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
        try:
            import huggingface_hub  # noqa: F401
            import jsonschema  # noqa: F401
        except Exception as exc:
            raise ImportError(
                "Required dependencies 'huggingface_hub' and 'jsonschema' are not installed."
            ) from exc

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
        from huggingface_hub import hf_hub_download

        repo_id = "chonkie/recipe-schema"
        filename = "schema.json"
        try:
            local_path = hf_hub_download(
                repo_id=repo_id, filename=filename, force_download=False)
        except Exception as exc:
            raise RuntimeError(
                f"Could not download schema from {repo_id}") from exc

        with open(local_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        return schema

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        from jsonschema import validate, ValidationError

        schema = self.get_recipe_schema()
        try:
            validate(instance=recipe, schema=schema)
            return True
        except ValidationError as exc:
            raise ValueError(
                f"Recipe validation failed: {exc.message}") from exc

    def get_recipe(
        self,
        recipe_name: Optional[str] = None,
        lang: Optional[str] = "en",
        path: Optional[str] = None,
    ) -> Optional[Dict]:
        '''Get a recipe from the hub.
        Args:
            recipe_name (Optional[str]): The name of the recipe to get.
            lang (Optional[str]): The language of the recipe to get.
            path (Optional[str]): Optionally, provide the path to the recipe.
        Returns:
            Optional[Dict]: The recipe.
        Raises:
            ValueError: If the recipe is not found.
            ValueError: If neither (recipe_name, lang) nor path are provided.
            ValueError: If the recipe is invalid.
        '''
        if path:
            # Load from local file
            if not os.path.exists(path):
                raise ValueError(f"Provided path does not exist: {path}")
            with open(path, "r", encoding="utf-8") as f:
                recipe = json.load(f)
        else:
            if not recipe_name:
                raise ValueError(
                    "Either recipe_name or path must be provided.")
            from huggingface_hub import hf_hub_download

            repo_id = "chonkie/recipes"
            filename = f"{lang}/{recipe_name}.json"
            try:
                local_path = hf_hub_download(
                    repo_id=repo_id, filename=filename, force_download=False)
            except Exception as exc:
                raise ValueError(
                    f"Could not find recipe '{recipe_name}' in language '{lang}'.") from exc

            with open(local_path, "r", encoding="utf-8") as f:
                recipe = json.load(f)

        # Validate the recipe
        self._validate_recipe(recipe)
        return recipe
