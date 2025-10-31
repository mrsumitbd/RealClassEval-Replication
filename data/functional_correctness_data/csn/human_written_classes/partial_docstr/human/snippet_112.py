from sacred.config.utils import dogmatize, normalize_or_die, recursive_fill_in
from sacred.config.signature import get_argspec
from sacred.config.config_summary import ConfigSummary
from sacred.utils import ConfigError
from copy import copy

class ConfigScope:

    def __init__(self, func):
        self.args, vararg_name, kw_wildcard, _, kwargs = get_argspec(func)
        assert vararg_name is None, '*args not allowed for ConfigScope functions'
        assert kw_wildcard is None, '**kwargs not allowed for ConfigScope functions'
        assert not kwargs, 'default values are not allowed for ConfigScope functions'
        self._func = func
        self._body_code = get_function_body_code(func)
        self._var_docs = get_config_comments(func)
        self.__doc__ = self._func.__doc__

    def __call__(self, fixed=None, preset=None, fallback=None):
        """
        Evaluate this ConfigScope.

        This will evaluate the function body and fill the relevant local
        variables into entries into keys in this dictionary.

        :param fixed: Dictionary of entries that should stay fixed during the
                      evaluation. All of them will be part of the final config.
        :type fixed: dict
        :param preset: Dictionary of preset values that will be available
                       during the evaluation (if they are declared in the
                       function argument list). All of them will be part of the
                       final config.
        :type preset: dict
        :param fallback: Dictionary of fallback values that will be available
                         during the evaluation (if they are declared in the
                         function argument list). They will NOT be part of the
                         final config.
        :type fallback: dict
        :return: self
        :rtype: ConfigScope
        """
        cfg_locals = dogmatize(fixed or {})
        fallback = fallback or {}
        preset = preset or {}
        fallback_view = {}
        available_entries = set(preset.keys()) | set(fallback.keys())
        for arg in self.args:
            if arg not in available_entries:
                raise KeyError("'{}' not in preset for ConfigScope. Available options are: {}".format(arg, available_entries))
            if arg in preset:
                cfg_locals[arg] = preset[arg]
            else:
                fallback_view[arg] = fallback[arg]
        cfg_locals.fallback = fallback_view
        with ConfigError.track(cfg_locals):
            eval(self._body_code, copy(self._func.__globals__), cfg_locals)
        added = cfg_locals.revelation()
        config_summary = ConfigSummary(added, cfg_locals.modified, cfg_locals.typechanges, cfg_locals.fallback_writes, docs=self._var_docs)
        recursive_fill_in(cfg_locals, preset)
        for key, value in cfg_locals.items():
            try:
                config_summary[key] = normalize_or_die(value)
            except ValueError:
                pass
        return config_summary