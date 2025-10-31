
class Config:

    def validate(self, config):
        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary")
        required_keys = ['template', 'version']
        for key in required_keys:
            if key not in config:
                raise KeyError(f"Missing required key: {key}")
        return True

    def get_template_from_config(self, config):
        self.validate(config)
        return config.get('template')
