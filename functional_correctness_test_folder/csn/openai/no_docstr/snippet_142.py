
class ProjectTemplate:
    @staticmethod
    def _get_common_data_template():
        """
        Return a dictionary containing the common project data template.
        """
        return {
            "name": "Default",
            "output_type": "exe",
            "build_dir": "build",
        }

    @staticmethod
    def _get_tool_specific_data_template():
        """
        Return a dictionary containing the tool‑specific project data template.
        """
        return {
            "debugger": None,
        }

    @staticmethod
    def get_project_template(name='Default', output_type='exe', debugger=None, build_dir='build'):
        """
        Build and return a complete project template dictionary.
        """
        common = ProjectTemplate._get_common_data_template()
        tool_specific = ProjectTemplate._get_tool_specific_data_template()

        # Override defaults with provided arguments
        common.update({
            "name": name,
            "output_type": output_type,
            "build_dir": build_dir,
        })
        tool_specific.update({
            "debugger": debugger,
        })

        # Merge the two dictionaries
        project_template = {**common, **tool_specific}
        return project_template
