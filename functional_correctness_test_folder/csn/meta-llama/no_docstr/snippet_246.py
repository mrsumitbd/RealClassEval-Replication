
import json
import jsonschema


class Config:

    def validate(self, config):
        """
        Validate the given configuration against a predefined schema.

        Args:
            config (dict): The configuration to be validated.

        Returns:
            bool: True if the configuration is valid, False otherwise.
        """
        schema = {
            "type": "object",
            "properties": {
                "template_name": {"type": "string"},
                "params": {"type": "object"}
            },
            "required": ["template_name", "params"]
        }

        try:
            jsonschema.validate(instance=config, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError:
            return False

    def get_template_from_config(self, config):
        """
        Extract the template name from the given configuration.

        Args:
            config (dict): The configuration containing the template name.

        Returns:
            str: The name of the template.

        Raises:
            ValueError: If the configuration is invalid.
        """
        if not self.validate(config):
            raise ValueError("Invalid configuration")

        return config["template_name"]


# Example usage:
if __name__ == "__main__":
    config = Config()
    valid_config = {
        "template_name": "example_template",
        "params": {
            "param1": "value1",
            "param2": "value2"
        }
    }
    invalid_config = {
        "template_name": "example_template"
    }

    print(config.validate(valid_config))  # Output: True
    print(config.validate(invalid_config))  # Output: False
    # Output: example_template
    print(config.get_template_from_config(valid_config))
    try:
        print(config.get_template_from_config(invalid_config))
    except ValueError as e:
        print(e)  # Output: Invalid configuration
