from typing import Optional, Dict, Any
import os
import json

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore


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
        self.repo_id: str = os.getenv('CHONKIE_HUB_REPO', 'chonkie-ai/recipes')
        self.repo_type: str = os.getenv('CHONKIE_HUB_REPO_TYPE', 'dataset')
        self.schema_path: str = os.getenv(
            'CHONKIE_HUB_SCHEMA_PATH', 'schema/recipe.schema.json')
        self.recipes_dir: str = os.getenv('CHONKIE_HUB_RECIPES_DIR', 'recipes')

        self._deps_ok: bool = False
        self.hf_hub_download = None  # type: ignore[assignment]
        self._jsonschema = None  # type: ignore[assignment]
        self._Draft7Validator = None  # type: ignore[assignment]

        self._schema_cache: Optional[Dict[str, Any]] = None

        self._import_dependencies()

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        self._deps_ok = bool(self._check_dependencies())
        if not self._deps_ok:
            return
        from huggingface_hub import hf_hub_download  # type: ignore
        import jsonschema  # type: ignore
        from jsonschema import Draft7Validator  # type: ignore

        self.hf_hub_download = hf_hub_download
        self._jsonschema = jsonschema
        self._Draft7Validator = Draft7Validator

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        try:
            import huggingface_hub  # noqa: F401
            import jsonschema  # noqa: F401
            if yaml is None:
                return False
            return True
        except Exception:
            return False

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        if not self._deps_ok or self.hf_hub_download is None:
            raise ValueError(
                'Required dependencies not available: huggingface_hub, jsonschema, pyyaml')

        if self._schema_cache is not None:
            return self._schema_cache

        schema_file = self.hf_hub_download(
            repo_id=self.repo_id, filename=self.schema_path, repo_type=self.repo_type
        )
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)

        self._schema_cache = schema
        return schema

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        if not self._deps_ok or self._jsonschema is None or self._Draft7Validator is None:
            return None
        schema = self.get_recipe_schema()
        try:
            self._Draft7Validator(schema).validate(recipe)
            return True
        except self._jsonschema.exceptions.ValidationError:
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
        if yaml is None:
            raise ValueError('Required dependency not available: pyyaml')

        if not path and not name:
            raise ValueError(
                'Either provide a recipe name (and optional lang) or a direct path')

        file_path: Optional[str] = None
        is_remote = False

        if path:
            if os.path.exists(path):
                file_path = path
            else:
                if not self._deps_ok or self.hf_hub_download is None:
                    raise ValueError(
                        'Required dependency not available to download from hub: huggingface_hub')
                file_path = self.hf_hub_download(
                    repo_id=self.repo_id, filename=path, repo_type=self.repo_type
                )
                is_remote = True
        else:
            if not self._deps_ok or self.hf_hub_download is None:
                raise ValueError(
                    'Required dependency not available to download from hub: huggingface_hub')
            tried = []
            for ext in ('yaml', 'yml', 'json'):
                candidate = f'{self.recipes_dir}/{lang}/{name}.{ext}'
                try:
                    file_path = self.hf_hub_download(
                        repo_id=self.repo_id, filename=candidate, repo_type=self.repo_type
                    )
                    is_remote = True
                    break
                except Exception:
                    tried.append(candidate)
                    continue
            if not file_path:
                raise ValueError(f'Recipe not found. Tried: {tried}')

        if not file_path or not os.path.exists(file_path):
            src = 'hub' if is_remote else 'filesystem'
            raise ValueError(
                f'Could not load recipe from {src} path: {file_path}')

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        with open(file_path, 'r', encoding='utf-8') as f:
            if ext in ('.yaml', '.yml'):
                recipe = yaml.safe_load(f)
            elif ext == '.json':
                recipe = json.load(f)
            else:
                # default to yaml
                recipe = yaml.safe_load(f)

        if not isinstance(recipe, dict):
            raise ValueError('Invalid recipe format: expected a mapping')

        valid = self._validate_recipe(recipe)
        if valid is False:
            raise ValueError('Invalid recipe: does not conform to schema')

        return recipe
