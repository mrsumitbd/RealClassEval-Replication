import os
import subprocess
import platform
import sys
import textwrap
import sysconfig
import re

class WindowsPython:
    """
    Windows only. Information about installed Python with specific word size
    and version. Defaults to the currently-running Python.

    Members:

        .path:
            Path of python binary.
        .version:
            `{major}.{minor}`, e.g. `3.9` or `3.11`. Same as `version` passed
            to `__init__()` if not None, otherwise the inferred version.
        .include:
            Python include path.
        .cpu:
            A `WindowsCpu` instance, same as `cpu` passed to `__init__()` if
            not None, otherwise the inferred cpu.

    We parse the output from `py -0p` to find all available python
    installations.
    """

    def __init__(self, cpu=None, version=None, verbose=True):
        """
        Args:

            cpu:
                A WindowsCpu instance. If None, we use whatever we are running
                on.
            version:
                Two-digit Python version as a string such as `3.8`. If None we
                use current Python's version.
            verbose:
                If true we show diagnostics.
        """
        if cpu is None:
            cpu = WindowsCpu(_cpu_name())
        if version is None:
            version = '.'.join(platform.python_version().split('.')[:2])
        _log(f'Looking for Python version={version!r} cpu.bits={cpu.bits!r}.')
        if '.'.join(platform.python_version().split('.')[:2]) == version:
            _log(f'cpu={cpu!r} version={version!r}: using sys.executable={sys.executable!r}.')
            self.path = sys.executable
            self.version = version
            self.cpu = cpu
            self.include = sysconfig.get_path('include')
        else:
            command = 'py -0p'
            if verbose:
                _log(f'cpu={cpu!r} version={version!r}: Running: {command}')
            text = subprocess.check_output(command, shell=True, text=True)
            for line in text.split('\n'):
                if (m := re.match('^ *-V:([0-9.]+)(-32)? ([*])? +(.+)$', line)):
                    version2 = m.group(1)
                    bits = 32 if m.group(2) else 64
                    current = m.group(3)
                    path = m.group(4).strip()
                elif (m := re.match('^ *-([0-9.]+)-((32)|(64)) +(.+)$', line)):
                    version2 = m.group(1)
                    bits = int(m.group(2))
                    path = m.group(5).strip()
                else:
                    if verbose:
                        _log(f'No match for line={line!r}')
                    continue
                if verbose:
                    _log(f'version2={version2!r} bits={bits!r} path={path!r} from line={line!r}.')
                if bits != cpu.bits or version2 != version:
                    continue
                root = os.path.dirname(path)
                if not os.path.exists(path):
                    assert path.endswith('.exe'), f'path={path!r}'
                    path2 = f'{path[:-4]}{version}.exe'
                    _log(f'Python {path!r} does not exist; changed to: {path2!r}')
                    assert os.path.exists(path2)
                    path = path2
                self.path = path
                self.version = version
                self.cpu = cpu
                command = f'''{self.path} -c "import sysconfig; print(sysconfig.get_path('include'))"'''
                _log(f'Finding Python include path by running command={command!r}.')
                self.include = subprocess.check_output(command, shell=True, text=True).strip()
                _log(f'Python include path is self.include={self.include!r}.')
                break
            else:
                _log(f'Failed to find python matching cpu={cpu}.')
                _log(f'Output from {command!r} was:\n{text}')
                raise Exception(f'Failed to find python matching cpu={cpu} version={version!r}.')
        self.libs = os.path.abspath(f'{self.include}/../libs')
        _log(f"WindowsPython:\n{self.description_ml('    ')}")

    def description_ml(self, indent=''):
        ret = textwrap.dedent(f'\n                path:       {self.path}\n                version:    {self.version}\n                cpu:        {self.cpu}\n                include:    {self.include}\n                libs:       {self.libs}\n                ')
        return textwrap.indent(ret, indent)

    def __repr__(self):
        return f'path={self.path!r} version={self.version!r} cpu={self.cpu!r} include={self.include!r} libs={self.libs!r}'