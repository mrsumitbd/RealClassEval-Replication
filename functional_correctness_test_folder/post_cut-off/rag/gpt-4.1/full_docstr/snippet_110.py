
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
        '''Initialize Hubbie.'''
        self._dependencies_checked = False
        self._hf_hub_download = None
        self._yaml = None
        self._jsonschema = None
        self._schema = None
        self._import_dependencies()

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            from huggingface_hub import hf_hub_download
            import yaml
            import jsonschema
            self._hf_hub_download = hf_hub_download
            self._yaml = yaml
            self._jsonschema = jsonschema
            self._dependencies_checked = True
        except ImportError as e:
            self._dependencies_checked = False
            raise ImportError(
                "Required dependencies for Hubbie are missing: huggingface_hub, pyyaml, jsonschema") from e

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        try:
            self._import_dependencies()
            return True
        except ImportError:
            return False

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        if not self._dependencies_checked:
            self._import_dependencies()
        if self._schema is not None:
            return self._schema
        # Download the schema from the hub
        # Assume repo_id and filename for schema
        repo_id = "chonkie/recipes"
        filename = "schema.yaml"
        try:
            schema_path = self._hf_hub_download(
                repo_id=repo_id, filename=filename)
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = self._yaml.safe_load(f)
            self._schema = schema
            return schema
        except Exception as e:
            raise RuntimeError(
                f"Could not fetch recipe schema from Huggingface Hub: {e}")

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        if not self._dependencies_checked:
            self._import_dependencies()
        schema = self.get_recipe_schema()
        try:
            self._jsonschema.validate(instance=recipe, schema=schema)
            return True
        except self._jsonschema.ValidationError as e:
            return False

    def get_recipe(self, recipe_name: str, lang: Optional[str] = 'en', path: Optional[str] = None) -> Optional[Dict]:
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
        if not self._dependencies_checked:
            self._import_dependencies()
        if path is not None:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    recipe = self._yaml.safe_load(f)
            except Exception as e:
                raise ValueError(
                    f"Could not load recipe from path {path}: {e}")
        elif recipe_name:
            repo_id = "chonkie/recipes"
            filename = f"{recipe_name}.{lang}.yaml"
            try:
                recipe_path = self._hf_hub_download(
                    repo_id=repo_id, filename=filename)
                with open(recipe_path, "r", encoding="utf-8") as f:
                    recipe = self._yaml.safe_load(f)
            except Exception as e:
                raise ValueError(
                    f"Could not fetch recipe '{recipe_name}' (lang={lang}) from Huggingface Hub: {e}")
        else:
            raise ValueError(
                "Either (recipe_name, lang) or path must be provided to get a recipe.")

        if not self._validate_recipe(recipe):
            raise ValueError(
                "The recipe is invalid according to the current schema.")
        return recipe
