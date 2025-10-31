class ProjectTemplate:

    @staticmethod
    def _get_common_data_template():
        return {
            'name': 'Default',
            'type': 'exe',
            'version': '1.0.0',
            'description': '',
            'entry_point': 'main',
            'debugger': None,
            'sources': [],
            'includes': [],
            'resources': [],
            'defines': [],
            'dependencies': [],
            'build': {
                'dir': 'build',
                'configuration': 'Debug',
                'configs': {
                    'Debug': {
                        'defines': ['DEBUG'],
                        'opt_level': 0,
                        'debug_symbols': True,
                        'warnings_as_errors': False
                    },
                    'Release': {
                        'defines': ['NDEBUG'],
                        'opt_level': 2,
                        'debug_symbols': False,
                        'warnings_as_errors': False
                    }
                }
            }
        }

    @staticmethod
    def _get_tool_specific_data_template():
        return {
            'tools': {
                'gcc': {
                    'cc': 'gcc',
                    'cxx': 'g++',
                    'ar': 'ar',
                    'ld': 'g++',
                    'defines_flag': '-D',
                    'include_flag': '-I',
                    'out_exe_flag': '-o',
                    'shared_flag': '-shared',
                    'std': {'c': 'c11', 'c++': 'c++17'},
                    'cflags': [],
                    'cxxflags': [],
                    'ldflags': [],
                    'env': {}
                },
                'clang': {
                    'cc': 'clang',
                    'cxx': 'clang++',
                    'ar': 'llvm-ar',
                    'ld': 'clang++',
                    'defines_flag': '-D',
                    'include_flag': '-I',
                    'out_exe_flag': '-o',
                    'shared_flag': '-shared',
                    'std': {'c': 'c11', 'c++': 'c++20'},
                    'cflags': [],
                    'cxxflags': [],
                    'ldflags': [],
                    'env': {}
                },
                'msvc': {
                    'cc': 'cl',
                    'cxx': 'cl',
                    'ar': 'lib',
                    'ld': 'link',
                    'defines_flag': '/D',
                    'include_flag': '/I',
                    'out_exe_flag': '/Fe:',
                    'out_obj_flag': '/Fo:',
                    'shared_flag': '/DLL',
                    'std': {'c': 'c11', 'c++': 'c++17'},
                    'cflags': [],
                    'cxxflags': [],
                    'ldflags': [],
                    'env': {}
                }
            }
        }

    @staticmethod
    def get_project_template(name='Default', output_type='exe', debugger=None, build_dir='build'):
        common = ProjectTemplate._get_common_data_template()
        tool_specific = ProjectTemplate._get_tool_specific_data_template()

        # Shallow merge since templates are disjoint at top-level
        template = {**common, **tool_specific}

        # Normalize output_type
        valid_types = {'exe', 'dll', 'shared', 'so', 'dylib', 'static', 'lib'}
        if output_type not in valid_types:
            output_type = 'exe'
        # Normalize to broad categories
        if output_type in {'dll', 'shared', 'so', 'dylib'}:
            normalized_type = 'shared'
        elif output_type in {'static', 'lib'}:
            normalized_type = 'static'
        else:
            normalized_type = 'exe'

        template['name'] = name
        template['type'] = normalized_type
        template['debugger'] = debugger
        template['build']['dir'] = build_dir

        return template
