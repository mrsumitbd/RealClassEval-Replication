
class ProjectTemplate:

    @staticmethod
    def _get_common_data_template():
        return {
            'name': 'Default',
            'version': '1.0',
            'description': '',
            'authors': [],
            'dependencies': []
        }

    @staticmethod
    def _get_tool_specific_data_template():
        return {
            'output_type': 'exe',
            'debugger': None,
            'build_dir': 'build',
            'compiler_flags': [],
            'linker_flags': []
        }

    @staticmethod
    def get_project_template(name='Default', output_type='exe', debugger=None, build_dir='build'):
        template = {
            'common': ProjectTemplate._get_common_data_template(),
            'tool_specific': ProjectTemplate._get_tool_specific_data_template()
        }
        template['common']['name'] = name
        template['tool_specific']['output_type'] = output_type
        template['tool_specific']['debugger'] = debugger
        template['tool_specific']['build_dir'] = build_dir
        return template
