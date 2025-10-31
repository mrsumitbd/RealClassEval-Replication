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
        if self._schema is not None:
            return self._schema
        repo_id = "chonkie/recipes"
        filename = "schema/recipe.schema.yaml"
        try:
            schema_path = self._hf_hub_download(
                repo_id=repo_id, filename=filename)
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = self._yaml.safe_load(f)
            self._schema = schema
            return schema
        except Exception as e:
            raise RuntimeError(
                f"Could not fetch recipe schema from Huggingface hub: {e}")

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        schema = self.get_recipe_schema()
        try:
            self._jsonschema.validate(instance=recipe, schema=schema)
            return True
        except self._jsonschema.ValidationError as e:
            return False

    def get_recipe(self, recipe_name: str, lang: Optional[str] = 'en') -> Optional[Dict]:
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
        repo_id = "chonkie/recipes"
        filename = f"recipes/{lang}/{recipe_name}.yaml"
        try:
            recipe_path = self._hf_hub_download(
                repo_id=repo_id, filename=filename)
        except Exception as e:
            raise ValueError(
                f"Recipe '{recipe_name}' (lang={lang}) not found on Huggingface hub: {e}")
        try:
            with open(recipe_path, "r", encoding="utf-8") as f:
                recipe = self._yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"Could not load recipe file: {e}")
        if not self._validate_recipe(recipe):
            raise ValueError(
                f"Recipe '{recipe_name}' is invalid according to the schema.")
        return recipe
