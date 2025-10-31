
import json
import jsonschema
from jsonschema import ValidationError


class Config:
    '''Provide tool to managed config
    '''

    def __init__(self, schema_path):
        """
        Initialize the Config class.

        Args:
        - schema_path (str): Path to the JSON schema file.
        """
        with open(schema_path, 'r') as schema_file:
            self.schema = json.load(schema_file)

    def validate(self, config):
        '''Validate that the source file is ok

        Args:
        - config (dict): Config object to be validated.

        Returns:
        - bool: True if the config is valid, False otherwise.

        Raises:
        - ValidationError: If the config is invalid.
        '''
        try:
            jsonschema.validate(instance=config, schema=self.schema)
            return True
        except ValidationError as e:
            raise ValidationError(f"Config is invalid: {e}")

    def get_template_from_config(self, config):
        '''Retrieve a template path from the config object

        Args:
        - config (dict): Config object.

        Returns:
        - str: Template path.

        Raises:
        - KeyError: If 'template' key is not found in the config.
        '''
        try:
            return config['template']
        except KeyError:
            raise KeyError("Config is missing 'template' key")


# Example usage:
if __name__ == "__main__":
    config = Config('config_schema.json')
    config_data = {
        "template": "path/to/template",
        # other config data...
    }
    try:
        if config.validate(config_data):
            print("Config is valid")
            template_path = config.get_template_from_config(config_data)
            print(f"Template path: {template_path}")
    except (ValidationError, KeyError) as e:
        print(e)
