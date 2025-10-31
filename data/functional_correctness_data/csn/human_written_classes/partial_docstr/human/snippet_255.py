import pathlib
import ruamel.yaml
from nornir.core.inventory import ConnectionOptions, Defaults, Group, Groups, Host, HostOrGroup, Hosts, Inventory, ParentGroups

class SimpleInventory:

    def __init__(self, host_file: str='hosts.yaml', group_file: str='groups.yaml', defaults_file: str='defaults.yaml', encoding: str='utf-8') -> None:
        """
        SimpleInventory is an inventory plugin that loads data from YAML files.
        The YAML files follow the same structure as the native objects

        Args:

          host_file: path to file with hosts definition
          group_file: path to file with groups definition. If
                it doesn't exist it will be skipped
          defaults_file: path to file with defaults definition.
                If it doesn't exist it will be skipped
          encoding: Encoding used to save inventory files. Defaults to utf-8
        """
        self.host_file = pathlib.Path(host_file).expanduser()
        self.group_file = pathlib.Path(group_file).expanduser()
        self.defaults_file = pathlib.Path(defaults_file).expanduser()
        self.encoding = encoding

    def load(self) -> Inventory:
        yml = ruamel.yaml.YAML(typ='safe')
        if self.defaults_file.exists():
            with open(self.defaults_file, 'r', encoding=self.encoding) as f:
                defaults_dict = yml.load(f) or {}
            defaults = _get_defaults(defaults_dict)
        else:
            defaults = Defaults()
        hosts = Hosts()
        with open(self.host_file, 'r', encoding=self.encoding) as f:
            hosts_dict = yml.load(f)
        for n, h in hosts_dict.items():
            hosts[n] = _get_inventory_element(Host, h, n, defaults)
        groups = Groups()
        if self.group_file.exists():
            with open(self.group_file, 'r', encoding=self.encoding) as f:
                groups_dict = yml.load(f) or {}
            for n, g in groups_dict.items():
                groups[n] = _get_inventory_element(Group, g, n, defaults)
            for g in groups.values():
                g.groups = ParentGroups([groups[g] for g in g.groups])
        for h in hosts.values():
            h.groups = ParentGroups([groups[g] for g in h.groups])
        return Inventory(hosts=hosts, groups=groups, defaults=defaults)