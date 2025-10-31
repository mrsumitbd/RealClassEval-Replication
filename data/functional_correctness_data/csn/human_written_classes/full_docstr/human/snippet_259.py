import yaml

class WCxf:
    """Base class for WCxf files (not meant to be used directly)."""

    @classmethod
    def load(cls, stream, **kwargs):
        """Load the object data from a JSON or YAML file."""
        wcxf = _load_yaml_json(stream, **kwargs)
        return cls(**wcxf)

    def dump(self, stream=None, fmt='json', **kwargs):
        """Dump the object data to a JSON or YAML file.

        Optional arguments:

        - `stream`: if None (default), return a string. Otherwise,
          should be a writable file-like object
        - `fmt`: format, should be 'json' (default) or 'yaml'

        Additional keyword arguments will be passed to the `json.dump(s)`
        or `yaml.dump` methods.
        """
        d = {k: v for k, v in self.__dict__.items() if k[0] != '_'}
        if fmt.lower() == 'json':
            indent = kwargs.pop('indent', 2)
            return _dump_json(d, stream=stream, indent=indent, **kwargs)
        elif fmt.lower() == 'yaml':
            default_flow_style = kwargs.pop('default_flow_style', False)
            return yaml.dump(d, stream, default_flow_style=default_flow_style, **kwargs)
        else:
            raise ValueError(f"Format {fmt} unknown: use 'json' or 'yaml'.")