
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Optional

# The class relies on two optional third‑party packages:
#   * huggingface_hub – to download files from the hub
#   * jsonschema      – to validate recipes against a JSON schema
# They are imported lazily so that the module can be imported even if the
# dependencies are missing.  The public API will raise a clear error if a
# method that requires a missing dependency is called.


class Hubbie:
    """Hubbie is a Huggingface hub manager for Chonkie.

    Methods
    -------
    get_recipe(recipe_name: str, lang: Optional[str] = 'en') -> Optional[Dict]:
        Get a recipe from the hub.
    get_recipe_schema() -> Dict:
        Get the current recipe schema from the hub.
    """

    # --------------------------------------------------------------------- #
    #  Construction and dependency handling
    # --------------------------------------------------------------------- #
    def __init__(self) -> None:
        """Initialize Hubbie."""
        self._import_dependencies()

    def _import_dependencies(self) -> None:
        """Check if the required dependencies are available and import them."""
        try:
            from huggingface_hub import hf_hub_download  # type: ignore
            self._hf_hub_download = hf_hub_download
        except Exception as exc:
            self._hf_hub_download = None
            self._hf_hub_import_error = exc

        try:
            from jsonschema import validate  # type: ignore
            self._jsonschema_validate = validate
        except Exception as exc:
            self._jsonschema_validate = None
            self._jsonschema_import_error = exc

    def _check_dependencies(self) -> Optional[bool]:
        """Check if the required dependencies are available."""
        return self._hf_hub_download is not None and self._jsonschema_validate is not None

    # --------------------------------------------------------------------- #
    #  Public API
    # --------------------------------------------------------------------- #
    def get_recipe_schema(self) -> Dict:
        """Get the current recipe schema from the hub."""
        if not self._check_dependencies():
            raise ImportError(
                "Required dependencies for Hubbie are missing. "
                f"hf_hub_import_error: {getattr(self, '_hf_hub_import_error', None)}, "
                f"jsonschema_import_error: {getattr(self, '_jsonschema_import_error', None)}"
            )

        # The schema is stored in the repository `chonkie/recipe-schema`
        # under the file `schema.json`.  We download it to a temporary
        # location and load it as JSON.
        repo_id = "chonkie/recipe-schema"
        filename = "schema.json"
        try:
            local_path = self._hf_hub_download(
                repo_id=repo_id, filename=filename, local_dir=None, force_download=True)
        except Exception as exc:
            raise RuntimeError(
                f"Could not download recipe schema from hub: {exc}") from exc

        with open(local_path, "r", encoding="utf-8") as f:
            schema = json.load(f)

        # Cache the schema on the instance to avoid repeated downloads.
        self._schema = schema
        return schema

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        """Validate a recipe against the current schema."""
        if not self._check_dependencies():
            raise ImportError(
                "Required dependencies for Hubbie are missing. "
                f"hf_hub_import_error: {getattr(self, '_hf_hub_import_error', None)}, "
                f"jsonschema_import_error: {getattr(self, '_jsonschema_import_error', None)}"
            )

        schema = getattr(self, "_schema", None)
        if schema is None:
            schema = self.get_recipe_schema()

        try:
            self._jsonschema_validate(instance=recipe, schema=schema)
        except Exception as exc:
            raise ValueError(f"Recipe validation failed: {exc}") from exc
        return True

    def get_recipe(
        self,
        recipe_name: str,
        lang: Optional[str] = "en",
        path: Optional[str] = None,
    ) -> Optional[Dict]:
        """Get a recipe from the hub.

        Parameters
        ----------
        recipe_name : str
            The name of the recipe to get.
        lang : Optional[str], default 'en'
            The language of the recipe to get.
        path : Optional[str]
            Optionally, provide the path to the recipe file.

        Returns
        -------
        Optional[Dict]
            The recipe as a dictionary.

        Raises
        ------
        ValueError
            If the recipe is not found.
        ValueError
            If neither (recipe_name, lang) nor path are provided.
        ValueError
            If the recipe is invalid.
        """
        if path is None:
            if not recipe_name:
                raise ValueError(
                    "Either recipe_name or path must be provided.")
            # Build the expected filename on the hub
            repo_id = "chonkie/recipes"
            filename = f"{recipe_name}_{lang}.json"
            try:
                local_path = self._hf_hub_download(
                    repo_id=repo_id, filename=filename, local_dir=None, force_download=True)
            except Exception as exc:
                raise ValueError(
                    f"Recipe '{recipe_name}' (lang={lang}) not found on hub: {exc}") from exc
        else:
            local_path = Path(path)
            if not local_path.is_file():
                raise ValueError(f"Provided path does not exist: {path}")

        # Load the recipe JSON
        try:
            with open(local_path, "r", encoding="utf-8") as f:
                recipe = json.load(f)
        except Exception as exc:
            raise ValueError(
                f"Could not load recipe JSON from {local_path}: {exc}") from exc

        # Validate the recipe
        self._validate_recipe(recipe)

        return recipe
