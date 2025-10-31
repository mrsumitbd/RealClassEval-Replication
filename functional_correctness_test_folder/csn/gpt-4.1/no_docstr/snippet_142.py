
class ProjectTemplate:

    @staticmethod
    def _get_common_data_template():
        return {
            'name': '',
            'output_type': '',
            'build_dir': '',
            'debugger': None
        }

    @staticmethod
    def _get_tool_specific_data_template():
        return {
            'compiler': '',
            'flags': [],
            'linker': '',
            'defines': [],
            'includes': []
        }

    @staticmethod
    def get_project_template(name='Default', output_type='exe', debugger=None, build_dir='build'):
        template = ProjectTemplate._get_common_data_template()
        tool_specific = ProjectTemplate._get_tool_specific_data_template()
        template.update({
            'name': name,
            'output_type': output_type,
            'build_dir': build_dir,
            'debugger': debugger
        })
        template['tool_specific'] = tool_specific
        return template
