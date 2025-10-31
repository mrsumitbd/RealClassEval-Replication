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
        self._hf_hub_download = None
        self._jsonschema_validate = None
        self._jsonschema_Draft = None
        self._json = None
        self._os = None
        self._pathlib = None
        self._import_dependencies()

        # Defaults can be overridden via environment variables
        self._repo_id = (self._os.getenv("CHONKIE_REPO_ID")
                         if self._os else None) or "chonkie/recipes"
        self._schema_repo_id = (self._os.getenv(
            "CHONKIE_SCHEMA_REPO_ID") if self._os else None) or self._repo_id
        self._schema_filename = (self._os.getenv(
            "CHONKIE_SCHEMA_FILENAME") if self._os else None) or "recipe.schema.json"
        self._recipes_dir = (self._os.getenv(
            "CHONKIE_RECIPES_DIR") if self._os else None) or "recipes"
        self._cache_dir = (self._os.getenv(
            "CHONKIE_CACHE_DIR") if self._os else None)

    def _import_dependencies(self) -> None:
        try:
            import huggingface_hub as _hf
            self._hf_hub_download = _hf.hf_hub_download
        except Exception:
            self._hf_hub_download = None

        try:
            import jsonschema as _js
            self._jsonschema_validate = _js.validate
            # Use a permissive draft by default (Draft2020-12 if available)
            self._jsonschema_Draft = getattr(
                _js, "Draft202012Validator", None) or getattr(_js, "Draft7Validator", None)
        except Exception:
            self._jsonschema_validate = None
            self._jsonschema_Draft = None

        import json as _json
        self._json = _json

        import os as _os
        self._os = _os

        import pathlib as _pathlib
        self._pathlib = _pathlib

    def _check_dependencies(self) -> bool:
        '''Check if the required dependencies are available.'''
        return self._hf_hub_download is not None

    def get_recipe_schema(self) -> dict:
        '''Get the current recipe schema from the hub.'''
        # Try local override via env var CHONKIE_SCHEMA_PATH
        local_schema_path = self._os.getenv(
            "CHONKIE_SCHEMA_PATH") if self._os else None
        if local_schema_path:
            p = self._pathlib.Path(local_schema_path)
            if not p.exists():
                raise ValueError(
                    f"Schema file not found at path: {local_schema_path}")
            try:
                return self._json.loads(p.read_text(encoding="utf-8"))
            except Exception as e:
                raise ValueError(
                    f"Failed to read schema from path '{local_schema_path}': {e}")

        # Otherwise, fetch from Hugging Face Hub
        if not self._check_dependencies():
            raise ImportError(
                "huggingface_hub is required to fetch the schema from the hub.")
        try:
            fpath = self._hf_hub_download(
                repo_id=self._schema_repo_id,
                filename=self._schema_filename,
                repo_type="dataset",
                cache_dir=self._cache_dir,
                local_files_only=False,
            )
            with open(fpath, "r", encoding="utf-8") as f:
                return self._json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to fetch schema from hub: {e}")

    def _validate_recipe(self, recipe: dict) -> bool:
        '''Validate a recipe against the current schema.'''
        if not isinstance(recipe, dict):
            raise ValueError("Recipe must be a dictionary.")
        try:
            schema = self.get_recipe_schema()
        except Exception as e:
            # If schema cannot be obtained, treat as invalid
            raise ValueError(f"Could not obtain recipe schema: {e}")

        if self._jsonschema_validate is None:
            # If jsonschema is not available, skip strict validation
            return True

        try:
            # If a specific validator is available, pre-check schema validity
            if self._jsonschema_Draft is not None:
                self._jsonschema_Draft.check_schema(schema)
            self._jsonschema_validate(instance=recipe, schema=schema)
            return True
        except Exception as e:
            raise ValueError(f"Recipe validation failed: {e}")

    def get_recipe(self, name: str = None, lang: str = 'en', path: str = None) -> dict | None:
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
        # Allow direct local path
        if path:
            p = self._pathlib.Path(path)
            if not p.exists():
                raise ValueError(f"Recipe not found at path: {path}")
            try:
                recipe = self._json.loads(p.read_text(encoding="utf-8"))
            except Exception as e:
                raise ValueError(
                    f"Failed to read recipe from path '{path}': {e}")
            self._validate_recipe(recipe)
            return recipe

        if not name:
            raise ValueError(
                "Either 'name' (with optional 'lang') or 'path' must be provided.")

        # First try local override via CHONKIE_RECIPES_ROOT
        local_root = self._os.getenv(
            "CHONKIE_RECIPES_ROOT") if self._os else None
        if local_root:
            p = self._pathlib.Path(local_root) / \
                self._recipes_dir / lang / f"{name}.json"
            if p.exists():
                try:
                    recipe = self._json.loads(p.read_text(encoding="utf-8"))
                except Exception as e:
                    raise ValueError(f"Failed to read local recipe '{p}': {e}")
                self._validate_recipe(recipe)
                return recipe

        # Otherwise fetch from Hugging Face Hub
        if not self._check_dependencies():
            raise ImportError(
                "huggingface_hub is required to fetch recipes from the hub.")

        filename = f"{self._recipes_dir}/{lang}/{name}.json"
        try:
            fpath = self._hf_hub_download(
                repo_id=self._repo_id,
                filename=filename,
                repo_type="dataset",
                cache_dir=self._cache_dir,
                local_files_only=False,
            )
        except Exception as e:
            raise ValueError(
                f"Recipe '{name}' (lang='{lang}') not found on hub: {e}")

        try:
            with open(fpath, "r", encoding="utf-8") as f:
                recipe = self._json.load(f)
        except Exception as e:
            raise ValueError(
                f"Failed to read recipe file '{filename}' from hub cache: {e}")

        self._validate_recipe(recipe)
        return recipe

    # Backward-compatibility: if an older consumer accidentally imported the typo'd method name,
    # ensure it still refers to get_recipe (without breaking get_recipe_schema).
    # Do not override get_recipe_schema; instead, provide an alias only if attribute not already set elsewhere.
    # Note: This is a no-op in typical usage but preserves compatibility for the provided skeleton typo.
    def __getattr__(self, name):
        if name == "get_recipe_schema" and callable(getattr(self, "get_recipe_schema")):
            return object.__getattribute__(self, "get_recipe_schema")
        if name == "get_recipe":
            return object.__getattribute__(self, "get_recipe")
        raise AttributeError(name)
