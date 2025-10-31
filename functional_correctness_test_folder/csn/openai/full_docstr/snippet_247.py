
import copy
from collections.abc import Mapping


class Merger:
    '''Provide tool to merge elements
    '''

    def _deep_merge(self, target, source):
        """Recursively merge source into target."""
        for key, value in source.items():
            if (
                key in target
                and isinstance(target[key], Mapping)
                and isinstance(value, Mapping)
            ):
                self._deep_merge(target[key], value)
            else:
                target[key] = copy.deepcopy(value)

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        '''Merge extended dicts

        Parameters
        ----------
        target : dict
            The dictionary to merge into.
        extends : list[dict]
            List of dictionaries to merge from.
        inherit_key : str, optional
            Key that indicates whether a dict should be merged.
        inherit : bool, optional
            If True, only merge dicts where ``inherit_key`` is truthy.
            If False, merge all dicts.

        Returns
        -------
        dict
            The merged dictionary (same object as ``target``).
        '''
        if not isinstance(target, Mapping):
            raise TypeError("target must be a mapping")
        if not isinstance(extends, (list, tuple)):
            raise TypeError("extends must be a list or tuple of mappings")

        for ext in extends:
            if not isinstance(ext, Mapping):
                continue
            if inherit:
                if not ext.get(inherit_key):
                    continue
            self._deep_merge(target, ext)
        return target

    def merge_sources(self, datas):
        '''Merge sources files

        Parameters
        ----------
        datas : list[dict]
            List of dictionaries to merge.

        Returns
        -------
        dict
            The merged dictionary.
        '''
        result = {}
        for data in datas:
            if isinstance(data, Mapping):
                self._deep_merge(result, data)
        return result

    def merge_configs(self, config, datas):
        '''Merge configs files

        Parameters
        ----------
        config : dict
            Base configuration dictionary.
        datas : list[dict]
            List of configuration dictionaries to merge into ``config``.

        Returns
        -------
        dict
            The merged configuration dictionary (same object as ``config``).
        '''
        if not isinstance(config, Mapping):
            raise TypeError("config must be a mapping")
        for data in datas:
            if isinstance(data, Mapping):
                self._deep_merge(config, data)
        return config
