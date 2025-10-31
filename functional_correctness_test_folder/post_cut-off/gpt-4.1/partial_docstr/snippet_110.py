
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
        self._import_dependencies()
        self._schema = None
        self._repo_id = "chonkie/recipes"
        self._schema_filename = "schema.json"
        self._recipes_dir = "recipes"
        self._check_dependencies()

    def _import_dependencies(self) -> None:
        global hf_hub_download, json, ValidationError, validate, jsonschema
        try:
            from huggingface_hub import hf_hub_download
        except ImportError:
            raise ImportError(
                "huggingface_hub is required. Please install it with 'pip install huggingface_hub'")
        try:
            import json
        except ImportError:
            raise ImportError("json module is required.")
        try:
            import jsonschema
            from jsonschema import validate, ValidationError
        except ImportError:
            raise ImportError(
                "jsonschema is required. Please install it with 'pip install jsonschema'")

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        try:
            from huggingface_hub import hf_hub_download
            import json
            import jsonschema
            from jsonschema import validate, ValidationError
            return True
        except ImportError:
            return False

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        if self._schema is not None:
            return self._schema
        try:
            schema_path = hf_hub_download(
                repo_id=self._repo_id, filename=self._schema_filename)
            with open(schema_path, "r", encoding="utf-8") as f:
                self._schema = json.load(f)
            return self._schema
        except Exception as e:
            raise RuntimeError(f"Could not fetch recipe schema: {e}")

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        schema = self.get_recipe_schema()
        try:
            validate(instance=recipe, schema=schema)
            return True
        except ValidationError:
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
        if not recipe_name:
            raise ValueError("Recipe name must be provided.")
        if not lang:
            lang = "en"
        filename = f"{self._recipes_dir}/{lang}/{recipe_name}.json"
        try:
            recipe_path = hf_hub_download(
                repo_id=self._repo_id, filename=filename)
        except Exception:
            raise ValueError(
                f"Recipe '{recipe_name}' (lang: {lang}) not found in the hub.")
        try:
            with open(recipe_path, "r", encoding="utf-8") as f:
                recipe = json.load(f)
        except Exception as e:
            raise ValueError(f"Could not load recipe: {e}")
        if not self._validate_recipe(recipe):
            raise ValueError("Recipe is invalid according to the schema.")
        return recipe
