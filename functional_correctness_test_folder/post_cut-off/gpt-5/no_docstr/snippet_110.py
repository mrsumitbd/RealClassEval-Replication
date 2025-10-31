from typing import Optional, Dict, Any
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
        self.repo_id: str = os.getenv("CHONKIE_HUB_REPO", "chonkie/recipes")
        self.repo_type: str = os.getenv("CHONKIE_HUB_REPO_TYPE", "dataset")
        self.schema_path: str = os.getenv(
            "CHONKIE_RECIPE_SCHEMA_PATH", "schemas/recipe.schema.json")
        self.recipe_dir: str = os.getenv("CHONKIE_RECIPE_DIR", "recipes")
        self._deps: Dict[str, Any] = {}
        self._cache: Dict[str, Any] = {
            "schema": None,
            "recipes": {}
        }
        self._import_dependencies()

    def _import_dependencies(self) -> None:
        try:
            import huggingface_hub as hf
            self._deps["hf"] = hf
        except Exception:
            self._deps["hf"] = None
        try:
            import jsonschema
            from jsonschema import validate
            self._deps["jsonschema"] = jsonschema
            self._deps["jsonschema_validate"] = validate
        except Exception:
            self._deps["jsonschema"] = None
            self._deps["jsonschema_validate"] = None

    def _check_dependencies(self) -> Optional[bool]:
        return bool(self._deps.get("hf") is not None)

    def _download_json_from_hub(self, filename: str) -> Optional[Dict]:
        hf = self._deps.get("hf")
        if hf is None:
            return None
        try:
            path = hf.hf_hub_download(
                repo_id=self.repo_id,
                filename=filename,
                repo_type=self.repo_type
            )
        except Exception:
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        if not isinstance(recipe, dict):
            return False
        schema = self.get_recipe_schema()
        if not schema:
            return True
        validator = self._deps.get("jsonschema_validate")
        if validator is None:
            return True
        try:
            validator(instance=recipe, schema=schema)
            return True
        except Exception:
            return False

    def get_recipe(self, recipe_name: str, lang: Optional[str] = 'en') -> Optional[Dict]:
        if not recipe_name:
            return None
        key = f"{lang}:{recipe_name}"
        if key in self._cache["recipes"]:
            return self._cache["recipes"][key]
        filename = f"{self.recipe_dir}/{lang}/{recipe_name}.json"
        data = self._download_json_from_hub(filename)
        if data is None:
            return None
        if not self._validate_recipe(data):
            return None
        self._cache["recipes"][key] = data
        return data

    def get_recipe_schema(self) -> Dict:
        if self._cache["schema"] is not None:
            return self._cache["schema"]
        data = self._download_json_from_hub(self.schema_path)
        if not isinstance(data, dict):
            data = {}
        self._cache["schema"] = data
        return data

    def get_recipe_schema(self) -> Dict:
        return self.get_recipe_schema()  # type: ignore
