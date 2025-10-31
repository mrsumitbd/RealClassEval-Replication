
class Config:
    '''Provide tool to managed config
    '''

    def validate(self, config):
        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary")
        if 'template_path' not in config:
            raise ValueError("Config must contain 'template_path'")

    def get_template_from_config(self, config):
        '''Retrieve a template path from the config object
        '''
        self.validate(config)
        return config['template_path']
