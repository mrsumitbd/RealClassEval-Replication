
from __future__ import annotations

import json
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

    def __init__(self) -> None:
        # Default repository containing recipes and schema
        self.repo_id: str = "chonkie/recipes"
        self._import_dependencies()
        if not self._check_dependencies():
            raise ImportError(
                "Required dependency 'huggingface_hub' is not installed."
            )

    def _import_dependencies(self) -> None:
        """Import optional dependencies lazily."""
        try:
            from huggingface_hub import hf_hub_download  # type: ignore
            self.hf_hub_download = hf_hub_download
        except Exception as exc:
            self.hf_hub_download = None
            self._dependency_error = exc

    def _check_dependencies(self) -> Optional[bool]:
        """Return True if dependencies are available, else False."""
        return self.hf_hub_download is not None

    def get_recipe_schema(self) -> Dict:
        """Fetch the recipe schema JSON from the hub."""
        if not self._check_dependencies():
            raise RuntimeError("huggingface_hub dependency is missing.")
        try:
            local_path = self.hf_hub_download(
                repo_id=self.repo_id,
                filename="schema.json",
                repo_type="dataset",
                local_dir=None,
                force_download=False,
            )
            with open(local_path, "r", encoding="utf-8") as f:
                schema = json.load(f)
            return schema
        except Exception as exc:
            raise RuntimeError(f"Failed to download schema: {exc}") from exc

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        """Basic validation: recipe must be a dict with required keys."""
        if not isinstance(recipe, dict):
            return False
        required_keys = {"name", "ingredients", "steps"}
        if not required_keys.issubset(recipe.keys()):
            return False
        return True

    def get_recipe(self, recipe_name: str, lang: Optional[str] = "en") -> Optional[Dict]:
        """Retrieve a recipe JSON from the hub."""
        if not self._check_dependencies():
            raise RuntimeError("huggingface_hub dependency is missing.")
        # Construct filename: e.g., "recipes/<recipe_name>_<lang>.json"
        filename = f"{recipe_name}_{lang}.json"
        try:
            local_path = self.hf_hub_download(
                repo_id=self.repo_id,
                filename=filename,
                repo_type="dataset",
                local_dir=None,
                force_download=False,
            )
            with open(local_path, "r", encoding="utf-8") as f:
                recipe = json.load(f)
            if not self._validate_recipe(recipe):
                raise ValueError(f"Recipe '{recipe_name}' failed validation.")
            return recipe
        except FileNotFoundError:
            # Try without language suffix
            filename = f"{recipe_name}.json"
            try:
                local_path = self.hf_hub_download(
                    repo_id=self.repo_id,
                    filename=filename,
                    repo_type="dataset",
                    local_dir=None,
                    force_download=False,
                )
                with open(local_path, "r", encoding="utf-8") as f:
                    recipe = json.load(f)
                if not self._validate_recipe(recipe):
                    raise ValueError(
                        f"Recipe '{recipe_name}' failed validation.")
                return recipe
            except Exception:
                return None
        except Exception as exc:
            raise RuntimeError(
                f"Failed to download recipe '{recipe_name}': {exc}") from exc
