from stevedore.extension import ExtensionManager
import functools
from collections import OrderedDict

class PluginManager:
    """
    Base class that manages plugins for an IDA.
    """

    @classmethod
    @functools.lru_cache(maxsize=None)
    def get_available_plugins(cls, namespace=None):
        """
        Returns a dict of all the plugins that have been made available.
        """
        plugins = OrderedDict()
        extension_manager = ExtensionManager(namespace=namespace or cls.NAMESPACE)
        for plugin_name in extension_manager.names():
            plugins[plugin_name] = extension_manager[plugin_name].plugin
        return plugins

    @classmethod
    def get_plugin(cls, name, namespace=None):
        """
        Returns the plugin with the given name.
        """
        plugins = cls.get_available_plugins(namespace)
        if name not in plugins:
            raise PluginError('No such plugin {name} for entry point {namespace}'.format(name=name, namespace=namespace or cls.NAMESPACE))
        return plugins[name]