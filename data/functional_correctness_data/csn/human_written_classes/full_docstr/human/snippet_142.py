class ProjectTemplate:
    """ Public data which can be set in yaml files
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
    """

    @staticmethod
    def _get_common_data_template():
        """ Data for tool specific """
        data_template = {'includes': [], 'linker_file': '', 'macros': [], 'sources': []}
        return data_template

    @staticmethod
    def _get_tool_specific_data_template():
        """ Data for tool specific """
        data_template = {'misc': {}, 'template': []}
        return data_template

    @staticmethod
    def get_project_template(name='Default', output_type='exe', debugger=None, build_dir='build'):
        """ Project data (+ data) """
        project_template = {'build_dir': build_dir, 'debugger': debugger, 'export_dir': '', 'name': name, 'output_type': output_type, 'target': '', 'tools_supported': []}
        project_template.update(ProjectTemplate._get_common_data_template())
        project_template.update(ProjectTemplate._get_tool_specific_data_template())
        return project_template