class WindowsCpu:
    """
    For Windows only. Paths and names that depend on cpu.

    Members:
        .bits
            32 or 64.
        .windows_subdir
            Empty string or `x64/`.
        .windows_name
            `x86` or `x64`.
        .windows_config
            `x64` or `Win32`, e.g. for use in `/Build Release|x64`.
        .windows_suffix
            `64` or empty string.
    """

    def __init__(self, name=None):
        if not name:
            name = _cpu_name()
        self.name = name
        if name == 'x32':
            self.bits = 32
            self.windows_subdir = ''
            self.windows_name = 'x86'
            self.windows_config = 'Win32'
            self.windows_suffix = ''
        elif name == 'x64':
            self.bits = 64
            self.windows_subdir = 'x64/'
            self.windows_name = 'x64'
            self.windows_config = 'x64'
            self.windows_suffix = '64'
        else:
            assert 0, f'Unrecognised cpu name: {name}'

    def __repr__(self):
        return self.name