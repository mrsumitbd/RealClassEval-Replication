
import json
import jsonschema


class Config:
    '''Provide tool to managed config
    '''

    def validate(self, config):
        """Validate the given config against a predefined schema."""
        schema = {
            "type": "object",
            "properties": {
                "template_path": {"type": "string"},
                # Add other expected properties here
            },
            # Adjust required fields as necessary
            "required": ["template_path"]
        }
        try:
            jsonschema.validate(instance=config, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as err:
            print(f"Config validation error: {err}")
            return False

    def get_template_from_config(self, config):
        '''Retrieve a template path from the config object'''
        if self.validate(config):
            return config.get('template_path')
        else:
            return None


# Example usage
if __name__ == "__main__":
    config_data = {
        "template_path": "/path/to/template"
    }
    config = Config()
    print(config.get_template_from_config(config_data))
