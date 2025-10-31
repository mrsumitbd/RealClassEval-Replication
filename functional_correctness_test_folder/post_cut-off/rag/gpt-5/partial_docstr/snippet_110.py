from typing import Optional, Dict, List
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
        self._deps_ok = None
        self._hf_hub_download = None
        self._hf_api = None
        self._jsonschema_validate = None
        self._jsonschema_module = None
        self._yaml = None

        # Defaults can be overridden via env vars
        self.repo_id = os.getenv('CHONKIE_HUB_REPO', 'chonkie/recipes')
        self.schema_candidates: List[str] = [
            os.getenv('CHONKIE_RECIPE_SCHEMA', 'recipe.schema.json'),
            'schema/recipe.schema.json',
            'schemas/recipe.schema.json',
        ]
        self.recipes_dir = os.getenv('CHONKIE_RECIPES_DIR', 'recipes')

        self._import_dependencies()

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            from huggingface_hub import hf_hub_download, HfApi  # type: ignore
            self._hf_hub_download = hf_hub_download
            self._hf_api = HfApi
        except Exception:
            self._hf_hub_download = None
            self._hf_api = None

        try:
            import jsonschema  # type: ignore
            from jsonschema import validate  # type: ignore
            self._jsonschema_validate = validate
            self._jsonschema_module = jsonschema
        except Exception:
            self._jsonschema_validate = None
            self._jsonschema_module = None

        try:
            import yaml  # type: ignore
            self._yaml = yaml
        except Exception:
            self._yaml = None

        self._deps_ok = self._hf_hub_download is not None

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        if self._deps_ok is None:
            self._import_dependencies()
        return bool(self._deps_ok)

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        if not self._check_dependencies():
            raise RuntimeError(
                'huggingface_hub is required to fetch the schema from the hub.')
        last_err = None
        for candidate in self.schema_candidates:
            try:
                local_path = self._hf_hub_download(
                    repo_id=self.repo_id, filename=candidate)
                with open(local_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                last_err = e
                continue
        raise FileNotFoundError(
            f'Could not locate recipe schema in repo {self.repo_id}. Last error: {last_err}')

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        if self._jsonschema_validate is None or self._jsonschema_module is None:
            return None
        schema = self.get_recipe_schema()
        # Optional schema validation check; ignore if not supported
        try:
            if hasattr(self._jsonschema_module, 'Draft202012Validator'):
                self._jsonschema_module.Draft202012Validator.check_schema(
                    schema)  # type: ignore[attr-defined]
            elif hasattr(self._jsonschema_module, 'Draft201909Validator'):
                self._jsonschema_module.Draft201909Validator.check_schema(
                    schema)  # type: ignore[attr-defined]
            elif hasattr(self._jsonschema_module, 'Draft7Validator'):
                self._jsonschema_module.Draft7Validator.check_schema(
                    schema)  # type: ignore[attr-defined]
        except Exception:
            pass
        self._jsonschema_validate(instance=recipe, schema=schema)
        return True

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
        # Local or direct path
        if path:
            try:
                loader = None
                if path.endswith('.json'):
                    with open(path, 'r', encoding='utf-8') as f:
                        recipe = json.load(f)
                elif path.endswith(('.yml', '.yaml')):
                    if self._yaml is None:
                        raise RuntimeError(
                            'PyYAML is required to load YAML recipes.')
                    with open(path, 'r', encoding='utf-8') as f:
                        recipe = self._yaml.safe_load(f)
                else:
                    # try json first, then yaml
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            recipe = json.load(f)
                    except Exception:
                        if self._yaml is None:
                            raise
                        with open(path, 'r', encoding='utf-8') as f:
                            recipe = self._yaml.safe_load(f)
                self._validate_recipe(recipe)
                return recipe
            except Exception as e:
                raise ValueError(
                    f'Failed to load recipe from path {path}: {e}') from e

        if not name or not lang:
            raise ValueError('Either provide a path or both name and lang.')

        # Fetch from hub
        if not self._check_dependencies():
            raise RuntimeError(
                'huggingface_hub is required to fetch recipes from the hub.')

        candidates = []
        base = self.recipes_dir.strip('/')

        # Common naming schemes
        candidates.extend([
            f'{base}/{name}/{lang}.yml',
            f'{base}/{name}/{lang}.yaml',
            f'{base}/{name}/{lang}.json',
            f'{base}/{name}-{lang}.yml',
            f'{base}/{name}-{lang}.yaml',
            f'{base}/{name}-{lang}.json',
            f'{base}/{name}.{lang}.yml',
            f'{base}/{name}.{lang}.yaml',
            f'{base}/{name}.{lang}.json',
            f'{name}-{lang}.yml',
            f'{name}-{lang}.yaml',
            f'{name}-{lang}.json',
            f'{name}.{lang}.yml',
            f'{name}.{lang}.yaml',
            f'{name}.{lang}.json',
        ])

        last_err = None
        for candidate in candidates:
            try:
                local_path = self._hf_hub_download(
                    repo_id=self.repo_id, filename=candidate)
                # parse
                if candidate.endswith('.json'):
                    with open(local_path, 'r', encoding='utf-8') as f:
                        recipe = json.load(f)
                elif candidate.endswith(('.yml', '.yaml')):
                    if self._yaml is None:
                        continue
                    with open(local_path, 'r', encoding='utf-8') as f:
                        recipe = self._yaml.safe_load(f)
                else:
                    with open(local_path, 'r', encoding='utf-8') as f:
                        try:
                            recipe = json.load(f)
                        except Exception:
                            if self._yaml is None:
                                continue
                            f.seek(0)
                            recipe = self._yaml.safe_load(f)
                self._validate_recipe(recipe)
                return recipe
            except Exception as e:
                last_err = e
                continue

        raise ValueError(
            f'Recipe "{name}" ({lang}) not found in repo {self.repo_id}. Last error: {last_err}')
