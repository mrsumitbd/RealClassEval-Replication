import os
import glob
import textwrap
import re

class WindowsVS:
    """
    Windows only. Finds locations of Visual Studio command-line tools. Assumes
    VS2019-style paths.

    Members and example values::

        .year:      2019
        .grade:     Community
        .version:   14.28.29910
        .directory: C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community
        .vcvars:    C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat
        .cl:        C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.28.29910\\bin\\Hostx64\\x64\\cl.exe
        .link:      C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.28.29910\\bin\\Hostx64\\x64\\link.exe
        .csc:       C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\MSBuild\\Current\\Bin\\Roslyn\\csc.exe
        .msbuild:   C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\MSBuild\\Current\\Bin\\MSBuild.exe
        .devenv:    C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\Common7\\IDE\\devenv.com

    `.csc` is C# compiler; will be None if not found.
    """

    def __init__(self, *, year=None, grade=None, version=None, cpu=None, directory=None, verbose=False):
        """
        Args:
            year:
                None or, for example, `2019`. If None we use environment
                variable WDEV_VS_YEAR if set.
            grade:
                None or, for example, one of:

                * `Community`
                * `Professional`
                * `Enterprise`

                If None we use environment variable WDEV_VS_GRADE if set.
            version:
                None or, for example: `14.28.29910`. If None we use environment
                variable WDEV_VS_VERSION if set.
            cpu:
                None or a `WindowsCpu` instance.
            directory:
                Ignore year, grade, version and cpu and use this directory
                directly.
            verbose:
                .

        """
        if year is not None:
            year = str(year)

        def default(value, name):
            if value is None:
                name2 = f'WDEV_VS_{name.upper()}'
                value = os.environ.get(name2)
                if value is not None:
                    _log(f'Setting {name} from environment variable {name2}: {value!r}')
            return value
        try:
            year = default(year, 'year')
            grade = default(grade, 'grade')
            version = default(version, 'version')
            if not cpu:
                cpu = WindowsCpu()
            if not directory:
                pattern = _vs_pattern(year, grade)
                directories = glob.glob(pattern)
                if verbose:
                    _log(f'Matches for: pattern={pattern!r}')
                    _log(f'directories={directories!r}')
                assert directories, f'No match found for pattern={pattern!r}.'
                directories.sort()
                directory = directories[-1]
            devenv = f'{directory}\\Common7\\IDE\\devenv.com'
            assert os.path.isfile(devenv), f'Does not exist: {devenv}'
            regex = f'^C:\\\\Program Files.*\\\\Microsoft Visual Studio\\\\([^\\\\]+)\\\\([^\\\\]+)'
            m = re.match(regex, directory)
            assert m, f'No match: regex={regex!r} directory={directory!r}'
            year2 = m.group(1)
            grade2 = m.group(2)
            if year:
                assert year2 == year
            else:
                year = year2
            if grade:
                assert grade2 == grade
            else:
                grade = grade2
            vcvars = f'{directory}\\VC\\Auxiliary\\Build\\vcvars{cpu.bits}.bat'
            assert os.path.isfile(vcvars), f'No match for: {vcvars}'
            cl_pattern = f"{directory}\\VC\\Tools\\MSVC\\{(version if version else '*')}\\bin\\Host{cpu.windows_name}\\{cpu.windows_name}\\cl.exe"
            cl_s = glob.glob(cl_pattern)
            assert cl_s, f'No match for: {cl_pattern}'
            cl_s.sort()
            cl = cl_s[-1]
            m = re.search(f'\\\\VC\\\\Tools\\\\MSVC\\\\([^\\\\]+)\\\\bin\\\\Host{cpu.windows_name}\\\\{cpu.windows_name}\\\\cl.exe$', cl)
            assert m
            version2 = m.group(1)
            if version:
                assert version2 == version
            else:
                version = version2
            assert version
            link_pattern = f'{directory}\\VC\\Tools\\MSVC\\{version}\\bin\\Host{cpu.windows_name}\\{cpu.windows_name}\\link.exe'
            link_s = glob.glob(link_pattern)
            assert link_s, f'No match for: {link_pattern}'
            link_s.sort()
            link = link_s[-1]
            csc = None
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    if filename == 'csc.exe':
                        csc = os.path.join(dirpath, filename)
            msbuild = None
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    if filename == 'MSBuild.exe':
                        msbuild = os.path.join(dirpath, filename)
            self.cl = cl
            self.devenv = devenv
            self.directory = directory
            self.grade = grade
            self.link = link
            self.csc = csc
            self.msbuild = msbuild
            self.vcvars = vcvars
            self.version = version
            self.year = year
            self.cpu = cpu
        except Exception as e:
            raise Exception(f'Unable to find Visual Studio year={year!r} grade={grade!r} version={version!r} cpu={cpu!r} directory={directory!r}') from e

    def description_ml(self, indent=''):
        """
        Return multiline description of `self`.
        """
        ret = textwrap.dedent(f'\n                year:         {self.year}\n                grade:        {self.grade}\n                version:      {self.version}\n                directory:    {self.directory}\n                vcvars:       {self.vcvars}\n                cl:           {self.cl}\n                link:         {self.link}\n                csc:          {self.csc}\n                msbuild:      {self.msbuild}\n                devenv:       {self.devenv}\n                cpu:          {self.cpu}\n                ')
        return textwrap.indent(ret, indent)

    def __repr__(self):
        items = list()
        for name in ('year', 'grade', 'version', 'directory', 'vcvars', 'cl', 'link', 'csc', 'msbuild', 'devenv', 'cpu'):
            items.append(f'{name}={getattr(self, name)!r}')
        return ' '.join(items)