
class ProjectTemplate:

    @staticmethod
    def _get_common_data_template():
        return {
            'name': '',
            'output_type': '',
            'debugger': None,
            'build_dir': ''
        }

    @staticmethod
    def _get_tool_specific_data_template():
        return {
            'compiler': '',
            'flags': [],
            'include_dirs': [],
            'lib_dirs': [],
            'libs': []
        }

    @staticmethod
    def get_project_template(name='Default', output_type='exe', debugger=None, build_dir='build'):
        project_template = ProjectTemplate._get_common_data_template()
        project_template.update(
            ProjectTemplate._get_tool_specific_data_template())

        project_template['name'] = name
        project_template['output_type'] = output_type
        project_template['debugger'] = debugger
        project_template['build_dir'] = build_dir

        return project_template
