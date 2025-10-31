class WCxf:
    '''Base class for WCxf files (not meant to be used directly).'''
    @classmethod
    def load(cls, stream, **kwargs):
        '''Load the object data from a JSON or YAML file.'''
        import json

        def _read_stream(s):
            if hasattr(s, 'read'):
                return s.read()
            return s

        text = _read_stream(stream)

        # Try JSON first
        try:
            if hasattr(stream, 'read'):
                # Re-parse from text to allow retrying YAML regardless of stream state
                return json.loads(text, **kwargs)
            else:
                return json.loads(text, **kwargs)
        except Exception:
            pass

        # Fallback to YAML
        try:
            import yaml
        except ImportError as e:
            raise ValueError(
                "Failed to parse as JSON; PyYAML not installed to try YAML.") from e

        try:
            return yaml.safe_load(text, **kwargs)
        except Exception as e:
            raise ValueError("Failed to parse input as JSON or YAML.") from e

    def dump(self, stream=None, fmt='json', **kwargs):
        '''Dump the object data to a JSON or YAML file.
        Optional arguments:
        - `stream`: if None (default), return a string. Otherwise,
          should be a writable file-like object
        - `fmt`: format, should be 'json' (default) or 'yaml'
        Additional keyword arguments will be passed to the `json.dump(s)`
        or `yaml.dump` methods.
        '''
        data = dict(self.__dict__)

        if fmt not in ('json', 'yaml'):
            raise ValueError("fmt must be 'json' or 'yaml'")

        if fmt == 'json':
            import json
            if stream is None:
                return json.dumps(data, **kwargs)
            json.dump(data, stream, **kwargs)
            return None

        # YAML
        try:
            import yaml
        except ImportError as e:
            raise ValueError("PyYAML is required for YAML output.") from e

        if stream is None:
            return yaml.safe_dump(data, **kwargs)
        yaml.safe_dump(data, stream, **kwargs)
        return None
