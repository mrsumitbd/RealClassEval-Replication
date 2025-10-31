
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
        self.hub_repo = "chonkie/recipes"
        self.schema_filename = "schema.json"
        self._schema = None

    def _import_dependencies(self) -> None:
        '''Check if the required dependencies are available and import them.'''
        try:
            global hf_hub_download
            from huggingface_hub import hf_hub_download
            global jsonschema
            import jsonschema
            global json
            import json
        except ImportError as e:
            raise ImportError(
                "Required dependencies not found: huggingface_hub, jsonschema, json") from e

    def _check_dependencies(self) -> Optional[bool]:
        '''Check if the required dependencies are available.'''
        try:
            import huggingface_hub
            import jsonschema
            import json
            return True
        except ImportError:
            return False

    def get_recipe_schema(self) -> Dict:
        '''Get the current recipe schema from the hub.'''
        if self._schema is not None:
            return self._schema
        schema_path = hf_hub_download(
            repo_id=self.hub_repo, filename=self.schema_filename)
        with open(schema_path, "r", encoding="utf-8") as f:
            self._schema = json.load(f)
        return self._schema

    def _validate_recipe(self, recipe: Dict) -> Optional[bool]:
        '''Validate a recipe against the current schema.'''
        schema = self.get_recipe_schema()
        try:
            jsonschema.validate(instance=recipe, schema=schema)
            return True
        except jsonschema.ValidationError:
            return False

    def get_recipe(self, recipe_name: str, lang: Optional[str] = 'en') -> Optional[Dict]:
        '''Get a recipe from the hub.
        Args:
            recipe_name (str): The name of the recipe to get.
            lang (Optional[str]): The language of the recipe to get.
        Returns:
            Optional[Dict]: The recipe.
        Raises:
            ValueError: If the recipe is not found.
            ValueError: If neither (name, lang) nor path are provided.
            ValueError: If the recipe is invalid.
        '''
        if not recipe_name:
            raise ValueError("Recipe name must be provided.")
        filename = f"{recipe_name}.{lang}.json" if lang else f"{recipe_name}.json"
        try:
            recipe_path = hf_hub_download(
                repo_id=self.hub_repo, filename=filename)
        except Exception as e:
            raise ValueError(
                f"Recipe '{recipe_name}' with lang '{lang}' not found on the hub.") from e
        with open(recipe_path, "r", encoding="utf-8") as f:
            import json
            recipe = json.load(f)
        if not self._validate_recipe(recipe):
            raise ValueError("The recipe is invalid according to the schema.")
        return recipe
