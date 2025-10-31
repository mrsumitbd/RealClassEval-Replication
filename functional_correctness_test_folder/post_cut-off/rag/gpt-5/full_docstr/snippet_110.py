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
        self.repo_id: str = (
            os.environ.get('CHONKIE_HUB_REPO')
            or os.environ.get('HUBBIE_REPO_ID')
            or 'chonkie/recipes'
        )
        self.repo_type: Optional[str] = os.environ.get(
            'CHONKIE_HUB_REPO_TYPE', 'dataset')
        self.revision: Optional[str] = os.environ.get('CHONKIE_HUB_REVISION')
        self._hf_hub_download = None
        self._jsonschema = None
        self._yaml = None
        self._schema: Optional[Dict] = None
        self._deps_ok: bool = False
        self._import_dependencies()

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            from huggingface_hub import hf_hub_download  # type: ignore
            self._hf_hub_download = hf_hub_download
        except Exception:
            self._hf_hub_download = None
        try:
            import jsonschema  # type: ignore
            self._jsonschema = jsonschema
        except Exception:
            self._jsonschema = None
        try:
            import yaml  # type: ignore
            self._yaml = yaml
        except Exception:
            self._yaml = None
        self._deps_ok = self._hf_hub_download is not None

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        return bool(self._deps_ok)

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        if self._schema is not None:
            return self._schema
        if not self._check_dependencies():
            raise ImportError(
                'huggingface_hub is required to fetch the recipe schema.')
        candidates = [
            'schemas/recipe.schema.json',
            'schema/recipe.schema.json',
            'recipe.schema.json',
            'schemas/recipe.json',
            'schema/recipe.json',
        ]
        last_err = None
        for filename in candidates:
            try:
                local_path = self._hf_hub_download(
                    repo_id=self.repo_id,
                    filename=filename,
                    repo_type=self.repo_type,
                    revision=self.revision,
                )
                with open(local_path, 'r', encoding='utf-8') as f:
                    schema = json.load(f)
                if isinstance(schema, dict):
                    self._schema = schema
                    return schema
            except Exception as e:
                last_err = e
                continue
        raise FileNotFoundError(
            f'Could not find recipe schema in repo {self.repo_id} '
            f'(repo_type={self.repo_type}, revision={self.revision}). Last error: {last_err}'
        )

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        try:
            schema = self.get_recipe_schema()
        except Exception:
            return True
        if self._jsonschema is None:
            return True
        try:
            # type: ignore[attr-defined]
            self._jsonschema.validate(instance=recipe, schema=schema)
            return True
        except Exception as e:
            raise ValueError(f'Invalid recipe: {e}') from e

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
        if not self._check_dependencies():
            raise ImportError('huggingface_hub is required to fetch recipes.')
        if not path and not name:
            raise ValueError(
                'Either "name" (with optional "lang") or "path" must be provided.')

        candidates = []
        if path:
            candidates.append(path)
        else:
            candidates.extend([
                f'recipes/{lang}/{name}.json',
                f'recipes/{lang}/{name}.yaml',
                f'recipes/{lang}/{name}.yml',
                f'recipe/{lang}/{name}.json',
                f'recipe/{lang}/{name}.yaml',
                f'recipe/{lang}/{name}.yml',
                f'{lang}/{name}.json',
                f'{lang}/{name}.yaml',
                f'{lang}/{name}.yml',
            ])

        last_err = None
        for filename in candidates:
            try:
                local_path = self._hf_hub_download(
                    repo_id=self.repo_id,
                    filename=filename,
                    repo_type=self.repo_type,
                    revision=self.revision,
                )
                with open(local_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                try:
                    data = json.loads(content)
                except Exception:
                    if self._yaml is None:
                        raise
                    # type: ignore[union-attr]
                    data = self._yaml.safe_load(content)
                if isinstance(data, dict):
                    self._validate_recipe(data)
                    return data
            except Exception as e:
                last_err = e
                continue

        raise ValueError(
            f'Recipe not found for name={name!r}, lang={lang!r}, path={path!r} in repo {self.repo_id}. '
            f'Last error: {last_err}'
        )
