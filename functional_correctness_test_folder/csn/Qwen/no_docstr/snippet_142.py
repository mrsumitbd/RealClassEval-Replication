
class ProjectTemplate:

    @staticmethod
    def _get_common_data_template():
        return {
            'name': 'Default',
            'output_type': 'exe',
            'build_dir': 'build'
        }

    @staticmethod
    def _get_tool_specific_data_template():
        return {
            'debugger': None,
            'compiler_flags': [],
            'linker_flags': []
        }

    @staticmethod
    def get_project_template(name='Default', output_type='exe', debugger=None, build_dir='build'):
        common_data = ProjectTemplate._get_common_data_template()
        tool_specific_data = ProjectTemplate._get_tool_specific_data_template()

        common_data['name'] = name
        common_data['output_type'] = output_type
        common_data['build_dir'] = build_dir
        tool_specific_data['debugger'] = debugger

        return {**common_data, **tool_specific_data}
