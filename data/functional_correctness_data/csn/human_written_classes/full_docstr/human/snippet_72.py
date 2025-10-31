from apio.common.apio_console import cout, cstyle
from dataclasses import dataclass
from typing import List, Callable, Tuple

@dataclass
class PackageScanResults:
    """Represents results of packages scan."""
    installed_ok_package_names: List[str]
    bad_version_package_names: List[str]
    uninstalled_package_names: List[str]
    broken_package_names: List[str]
    orphan_package_names: List[str]
    orphan_dir_names: List[str]
    orphan_file_names: List[str]

    def packages_installed_ok(self) -> bool:
        """Returns true if all packages are installed ok, regardless of
        other fixable errors."""
        return len(self.bad_version_package_names) == 0 and len(self.uninstalled_package_names) == 0 and (len(self.broken_package_names) == 0)

    def num_errors_to_fix(self) -> bool:
        """Returns the number of errors that required , having a non installed
        packages is not considered an error that need to be fix."""
        return len(self.bad_version_package_names) + len(self.broken_package_names) + len(self.orphan_package_names) + len(self.orphan_dir_names) + len(self.orphan_file_names)

    def is_all_ok(self) -> bool:
        """Return True if all packages are installed properly with no
        issues."""
        return not self.num_errors_to_fix() and (not self.uninstalled_package_names)

    def dump(self):
        """Dump the content of this object. For debugging."""
        cout()
        cout('Package scan results:')
        cout(f'  Installed     {self.installed_ok_package_names}')
        cout(f'  bad version   {self.bad_version_package_names}')
        cout(f'  Uninstalled   {self.uninstalled_package_names}')
        cout(f'  Broken        {self.broken_package_names}')
        cout(f'  Orphan ids    {self.orphan_package_names}')
        cout(f'  Orphan dirs   {self.orphan_dir_names}')
        cout(f'  Orphan files  {self.orphan_file_names}')