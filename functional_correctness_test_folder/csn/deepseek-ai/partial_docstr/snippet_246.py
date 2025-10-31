
class Config:
    '''Provide tool to managed config
    '''

    def validate(self, config):
        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary")
        required_keys = ['template_path', 'settings']
        for key in required_keys:
            if key not in config:
                raise KeyError(f"Missing required key in config: {key}")
        return True

    def get_template_from_config(self, config):
        '''Retrieve a template path from the config object
        '''
        self.validate(config)
        return config.get('template_path')
