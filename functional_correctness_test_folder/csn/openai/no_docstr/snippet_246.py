
class Config:
    def validate(self, config):
        if not isinstance(config, dict):
            raise TypeError("config must be a dictionary")
        if "template" not in config:
            raise KeyError("config missing required 'template' key")
        if not isinstance(config["template"], str):
            raise TypeError("'template' value must be a string")
        return True

    def get_template_from_config(self, config):
        self.validate(config)
        return config["template"]
