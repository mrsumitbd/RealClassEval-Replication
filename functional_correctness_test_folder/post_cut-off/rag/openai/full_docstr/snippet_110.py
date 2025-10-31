
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

    # Default repository that contains the recipes and the schema
    _REPO_ID = "chonkie/recipes"
    _SCHEMA_FILE = "recipe_schema.json"

    def __init__(self) -> None:
        '''Initialize Hubbie.'''
        self._import_dependencies()
        self._schema: Optional[Dict] = None

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            from huggingface_hub import hf_hub_download  # noqa: F401
            from jsonschema import validate  # noqa: F401
        except Exception as exc:
            raise ImportError(
                "Hubbie requires the 'huggingface_hub' and 'jsonschema' packages. "
                f"Original error: {exc}"
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
        if self._schema is not None:
            return self._schema

        from huggingface_hub import hf_hub_download

        try:
            schema_path = hf_hub_download(
                repo_id=self._REPO_ID,
                filename=self._SCHEMA_FILE,
                repo_type="dataset",
            )
        except Exception as exc:
            raise ValueError(
                f"Could not download recipe schema from repo '{self._REPO_ID}'. "
                f"Original error: {exc}"
            ) from exc

        with open(schema_path, "r", encoding="utf-8") as f:
            self._schema = json.load(f)

        return self._schema

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
            recipe_path = Path(path)
            if not recipe_path.is_file():
                raise ValueError(
                    f"Provided path '{path}' does not exist or is not a file.")
            with open(recipe_path, "r", encoding="utf-8") as f:
                recipe = json.load(f)
        else:
            if not recipe_name:
                raise ValueError(
                    "Either recipe_name (with optional lang) or path must be provided.")
            # Build filename
            filename = f"{recipe_name}_{lang}.json"
            from huggingface_hub import hf_hub_download

            try:
                recipe_path = hf_hub_download(
                    repo_id=self._REPO_ID,
                    filename=filename,
                    repo_type="dataset",
                )
            except Exception as exc:
                raise ValueError(
                    f"Could not download recipe '{recipe_name}' (lang={lang}) from repo '{self._REPO_ID}'. "
                    f"Original error: {exc}"
                ) from exc

            with open(recipe_path, "r", encoding="utf-8") as f:
                recipe = json.load(f)

        # Validate recipe
        self._validate_recipe(recipe)

        return recipe
