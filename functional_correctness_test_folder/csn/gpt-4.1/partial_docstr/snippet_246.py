
class Config:
    '''Provide tool to managed config
    '''

    def validate(self, config):
        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary.")
        if 'template' not in config:
            raise ValueError("Config must contain a 'template' key.")
        if not isinstance(config['template'], str) or not config['template']:
            raise ValueError("'template' must be a non-empty string.")

    def get_template_from_config(self, config):
        '''Retrieve a template path from the config object
        '''
        self.validate(config)
        return config['template']
