
class ProjectTemplate:
    ''' Public data which can be set in yaml files
        Yaml data available are:
            'build_dir' : build_dir,    # Build output path
            'debugger' : debugger,      # Debugger
            'export_dir': '',           # Export directory path
            'includes': [],             # include paths
            'linker_file': None,        # linker script file
            'name': name,               # project name
            'macros': [],               # macros
            'misc': {},                 # misc settings related to tools
            'output_type': output_type, # output type, default - exe
            'sources': [],              # source files/folders
            'target': '',               # target
            'template' : [],            # tool template
            'tools_supported': [],      # Tools which are supported,
    '''
    @staticmethod
    def _get_common_data_template():
        ''' Data for tool specific '''
        return {
            'build_dir': '',
            'debugger': None,
            'export_dir': '',
            'includes': [],
            'linker_file': None,
            'name': '',
            'macros': [],
            'misc': {},
            'output_type': 'exe',
            'sources': [],
            'target': '',
            'template': [],
            'tools_supported': []
        }

    @staticmethod
    def _get_tool_specific_data_template():
        ''' Data for tool specific '''
        return {
            'compiler': None,
            'linker': None,
            'build_flags': [],
            'link_flags': [],
            'debugger': None
        }

    @staticmethod
    def get_project_template(name='Default', output_type='exe', debugger=None, build_dir='build'):
        ''' Project data (+ data) '''
        data = ProjectTemplate._get_common_data_template()
        data.update(ProjectTemplate._get_tool_specific_data_template())
        data['name'] = name
        data['output_type'] = output_type
        data['debugger'] = debugger
        data['build_dir'] = build_dir
        return data
