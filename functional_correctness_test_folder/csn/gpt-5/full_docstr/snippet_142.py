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
            'name': 'Default',
            'output_type': 'exe',
            'debugger': None,
            'build_dir': 'build',
            'export_dir': '',
            'includes': [],
            'linker_file': None,
            'macros': [],
            'misc': {},
            'sources': [],
            'target': '',
            'template': [],
            'tools_supported': [],
        }

    @staticmethod
    def _get_tool_specific_data_template():
        ''' Data for tool specific '''
        return {}

    @staticmethod
    def get_project_template(name='Default', output_type='exe', debugger=None, build_dir='build'):
        ''' Project data (+ data) '''
        data = ProjectTemplate._get_common_data_template()
        # Ensure new containers to avoid shared state between calls
        data['includes'] = list(data.get('includes', []))
        data['macros'] = list(data.get('macros', []))
        data['misc'] = dict(data.get('misc', {}))
        data['sources'] = list(data.get('sources', []))
        data['template'] = list(data.get('template', []))
        data['tools_supported'] = list(data.get('tools_supported', []))

        data['name'] = name
        data['output_type'] = output_type
        data['debugger'] = debugger
        data['build_dir'] = build_dir

        tool_specific = ProjectTemplate._get_tool_specific_data_template()
        # Merge tool-specific data if any (kept separate under a dedicated key)
        if tool_specific:
            data['tool_specific'] = tool_specific

        return data
