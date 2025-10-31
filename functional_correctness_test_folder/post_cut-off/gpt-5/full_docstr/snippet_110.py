from typing import Optional, Dict
import os
import json


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
        self._hf_api = None
        self._hf_download = None
        self._jsonschema = None
        self._import_dependencies()
        self.repo_id = os.getenv("CHONKIE_RECIPE_REPO", "ChonkieAI/recipes")
        self.schema_path = os.getenv(
            "CHONKIE_RECIPE_SCHEMA_PATH", "schema/recipe.schema.json")
        self.recipe_base_path = os.getenv(
            "CHONKIE_RECIPE_BASE_PATH", "recipes")
        self._cached_schema: Optional[Dict] = None

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            from huggingface_hub import HfApi, hf_hub_download
            self._hf_api = HfApi
            self._hf_download = hf_hub_download
        except Exception:
            self._hf_api = None
            self._hf_download = None
        try:
            import jsonschema
            self._jsonschema = jsonschema
        except Exception:
            self._jsonschema = None

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        return bool(self._hf_download)

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        if self._cached_schema is not None:
            return self._cached_schema
        default_schema: Dict = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Chonkie Recipe",
            "type": "object",
            "required": ["name", "lang", "version"],
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "lang": {"type": "string", "minLength": 2},
                "version": {"type": "string", "minLength": 1},
                "description": {"type": "string"},
                "steps": {
                    "type": "array",
                    "items": {"type": "object"},
                },
                "meta": {"type": "object"},
            },
            "additionalProperties": True,
        }
        if not self._check_dependencies():
            self._cached_schema = default_schema
            return self._cached_schema
        try:
            file_path = self._hf_download(
                repo_id=self.repo_id, filename=self.schema_path)
            with open(file_path, "r", encoding="utf-8") as f:
                self._cached_schema = json.load(f)
            return self._cached_schema
        except Exception:
            self._cached_schema = default_schema
            return self._cached_schema

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        if not isinstance(recipe, dict):
            return False
        schema = self.get_recipe_schema()
        if self._jsonschema is None:
            required = schema.get("required", [])
            for key in required:
                if key not in recipe:
                    return False
            return True
        try:
            self._jsonschema.validate(instance=recipe, schema=schema)
            return True
        except Exception:
            return False

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
        if path is None and not name:
            raise ValueError(
                "Either path or (name and lang) must be provided.")
        data: Optional[Dict] = None
        if path:
            if not os.path.exists(path):
                raise ValueError(f"Recipe not found at path: {path}")
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            if not lang:
                raise ValueError(
                    "Language must be provided when fetching by name.")
            filename = f"{self.recipe_base_path}/{lang}/{name}.json"
            if not self._check_dependencies():
                raise ValueError(
                    "huggingface_hub is not available to download the recipe.")
            try:
                file_path = self._hf_download(
                    repo_id=self.repo_id, filename=filename)
            except Exception as e:
                raise ValueError(
                    f"Recipe '{name}' with lang '{lang}' not found: {e}")
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        if not self._validate_recipe(data):
            raise ValueError("Recipe is invalid against the schema.")
        return data
