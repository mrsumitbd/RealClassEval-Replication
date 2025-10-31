import re

class ParsedPipDeclaration:

    def __init__(self, declaration):
        self.pkgname = None
        self.specification = None
        self.flags = []
        self.is_editable = False
        self.path = None
        self._parse_declaration(declaration)
        if not self.pkgname and (not self.path):
            raise ValueError('Either a valid package name or a path must be present in the declaration.')

    def _parse_declaration(self, declaration):
        flag_with_value_pattern = '(--[\\w-]+=\\"[^\\"]+\\")'
        flag_values = re.findall(flag_with_value_pattern, declaration)
        for flag_value in flag_values:
            self.flags.append(flag_value)
            declaration = declaration.replace(flag_value, '', 1)
        git_url_pattern = '(git\\+https:\\/\\/[a-zA-Z0-9-_\\/.]+)(?:@([a-zA-Z0-9-_\\/.]+))?(?:#egg=([a-zA-Z0-9-_]+))?'
        git_url_match = re.search(git_url_pattern, declaration)
        if git_url_match:
            self.path = git_url_match.group(1)
            branch_or_tag = git_url_match.group(2)
            if branch_or_tag:
                self.path += f'@{branch_or_tag}'
            if git_url_match.group(3):
                self.pkgname = git_url_match.group(3)
            declaration = declaration.replace(git_url_match.group(0), '', 1)
        local_pattern = '(\\.\\/[a-zA-Z0-9-_]+\\/?|\\.\\.\\/[a-zA-Z0-9-_]+\\/?|\\/\\w+\\/?)'
        local_match = re.search(local_pattern, declaration)
        if local_match:
            self.path = local_match.group(1)
            declaration = declaration.replace(local_match.group(0), '', 1)
        flags_pattern = '(?:^|\\s)(-[a-zA-Z]|--\\w+(?:-\\w+)*)'
        flags = re.findall(flags_pattern, declaration)
        if flags:
            self.flags.extend(flags)
            if '-e' in self.flags:
                self.is_editable = True
        for flag in self.flags:
            declaration = declaration.replace(flag, '', 1)
        pkg_pattern = '(?P<name>[a-zA-Z0-9-_]+)(((?P<specifier>[<>!=~]{1,2})(?P<version>[0-9.a-zA-Z_-]+))((?P<multi_spec>,[<>!=~]{1,2}[0-9.a-zA-Z_-]+)*)?)?'
        pkg_match = re.search(pkg_pattern, declaration)
        if pkg_match:
            self.pkgname = pkg_match.group('name')
            specifier = pkg_match.group('specifier')
            version = pkg_match.group('version')
            multi_spec = pkg_match.group('multi_spec')
            if specifier:
                self.specification = f"{specifier}{version}{multi_spec or ''}"
            else:
                declaration = declaration.replace(pkg_match.group('name'), '', 1)
                version_match = re.search('(?P<version>\\d+(\\.\\d+)*([a-zA-Z0-9]+)?)', declaration)
                if version_match:
                    self.specification = f'=={version_match.group(0)}'