
class Config:

    def validate(self, config):

        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary")

        required_keys = ['template', 'variables']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Config must contain the key: {key}")

        if not isinstance(config['template'], str):
            raise ValueError("Template must be a string")

        if not isinstance(config['variables'], dict):
            raise ValueError("Variables must be a dictionary")

    def get_template_from_config(self, config):

        self.validate(config)
        return config['template']
