class BasePathMapper:
    match_type: str

    def __init__(self, config):
        action_type = config.get('action', DEFAULT_MAPPED_ACTION)
        action_class = actions.get(action_type, None)
        action_kwds = action_class.action_spec.copy()
        for key, value in action_kwds.items():
            if key in config:
                action_kwds[key] = config[key]
            elif value is REQUIRED_ACTION_KWD:
                message_template = 'action_type %s requires key word argument %s'
                message = message_template % (action_type, key)
                raise Exception(message)
            else:
                action_kwds[key] = value
        self.action_type = action_type
        self.action_kwds = action_kwds
        path_types_str = config.get('path_types', '*defaults*')
        path_types_str = path_types_str.replace('*defaults*', ','.join(ACTION_DEFAULT_PATH_TYPES))
        path_types_str = path_types_str.replace('*any*', ','.join(ALL_PATH_TYPES))
        self.path_types = path_types_str.split(',')
        self.file_lister = FileLister(config)

    def matches(self, path, path_type):
        path_type_matches = path_type in self.path_types
        rval = path_type_matches and self._path_matches(path)
        return rval

    def _extend_base_dict(self, **kwds):
        base_dict = dict(action=self.action_type, path_types=','.join(self.path_types), match_type=self.match_type)
        base_dict.update(self.file_lister.to_dict())
        base_dict.update(self.action_kwds)
        base_dict.update(**kwds)
        return base_dict

    def to_pattern(self):
        raise NotImplementedError()