
class Config:

    def validate(self, config):
        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary")
        required_keys = {'host', 'port', 'use_ssl'}
        if not required_keys.issubset(config.keys()):
            raise KeyError(
                f"Config must contain the following keys: {required_keys}")
        if not isinstance(config['host'], str):
            raise ValueError("Host must be a string")
        if not isinstance(config['port'], int):
            raise ValueError("Port must be an integer")
        if not isinstance(config['use_ssl'], bool):
            raise ValueError("Use_ssl must be a boolean")

    def get_template_from_config(self, config):
        self.validate(config)
        template = f"Host: {config['host']}\nPort: {config['port']}\nUse SSL: {config['use_ssl']}"
        return template
