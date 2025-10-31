
from typing import Optional, Dict


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
        self._schema_repo = "chonkie/recipe-schema"
        self._recipes_repo = "chonkie/recipes"
        self._schema_filename = "schema.json"
        self._hf = None

    def _import_dependencies(self) -> None:
        try:
            import huggingface_hub
            import json
            self._hf = huggingface_hub
            self._json = json
        except ImportError as e:
            self._hf = None
            self._json = None
            raise ImportError("huggingface_hub and json are required") from e

    def _check_dependencies(self) -> Optional[bool]:
        return self._hf is not None and self._json is not None

    def get_recipe_schema(self) -> Dict:
        if not self._check_dependencies():
            self._import_dependencies()
        file_content = self._hf.hf_hub_download(
            repo_id=self._schema_repo,
            filename=self._schema_filename
        )
        with open(file_content, "r", encoding="utf-8") as f:
            schema = self._json.load(f)
        return schema

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        schema = self.get_recipe_schema()
        # Simple validation: check required keys
        required_keys = schema.get("required", [])
        for key in required_keys:
            if key not in recipe:
                return False
        return True

    def get_recipe(self, recipe_name: str, lang: Optional[str] = 'en') -> Optional[Dict]:
        if not self._check_dependencies():
            self._import_dependencies()
        filename = f"{recipe_name}_{lang}.json"
        try:
            file_content = self._hf.hf_hub_download(
                repo_id=self._recipes_repo,
                filename=filename
            )
            with open(file_content, "r", encoding="utf-8") as f:
                recipe = self._json.load(f)
            if self._validate_recipe(recipe):
                return recipe
            else:
                return None
        except Exception:
            return None
