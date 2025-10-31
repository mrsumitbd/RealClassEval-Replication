import os
from typing import TYPE_CHECKING, Any, Optional, Union, cast
import argparse

class DependenciesConfiguration:
    """Dependency configuration class, for RuntimeContext.job_script_provider."""

    def __init__(self, args: argparse.Namespace) -> None:
        """Initialize."""
        self.tool_dependency_dir: Optional[str] = None
        self.dependency_resolvers_config_file: Optional[str] = None
        conf_file = getattr(args, 'beta_dependency_resolvers_configuration', None)
        tool_dependency_dir = getattr(args, 'beta_dependencies_directory', None)
        conda_dependencies = getattr(args, 'beta_conda_dependencies', None)
        if conf_file is not None and os.path.exists(conf_file):
            self.use_tool_dependencies = True
            if tool_dependency_dir is None:
                tool_dependency_dir = os.path.abspath(os.path.dirname(conf_file))
            self.tool_dependency_dir = tool_dependency_dir
            self.dependency_resolvers_config_file = os.path.abspath(conf_file)
        elif conda_dependencies is not None:
            if tool_dependency_dir is None:
                tool_dependency_dir = os.path.abspath('./cwltool_deps')
            self.tool_dependency_dir = tool_dependency_dir
            self.use_tool_dependencies = True
            self.dependency_resolvers_config_file = None
        else:
            self.use_tool_dependencies = False
        if self.tool_dependency_dir and (not os.path.exists(self.tool_dependency_dir)):
            os.makedirs(self.tool_dependency_dir)

    def build_job_script(self, builder: 'Builder', command: list[str]) -> str:
        """Use the galaxy-tool-util library to construct a build script."""
        ensure_galaxy_lib_available()
        resolution_config_dict = {'use': self.use_tool_dependencies, 'default_base_path': self.tool_dependency_dir}
        app_config = {'conda_auto_install': True, 'conda_auto_init': True, 'debug': builder.debug}
        tool_dependency_manager: 'deps.DependencyManager' = deps.build_dependency_manager(app_config_dict=app_config, resolution_config_dict=resolution_config_dict, conf_file=self.dependency_resolvers_config_file)
        handle_dependencies: str = ''
        if (dependencies := get_dependencies(builder)):
            handle_dependencies = '\n'.join(tool_dependency_manager.dependency_shell_commands(dependencies, job_directory=builder.tmpdir))
        template_kwds: dict[str, str] = dict(handle_dependencies=handle_dependencies)
        job_script = COMMAND_WITH_DEPENDENCIES_TEMPLATE.substitute(template_kwds)
        return job_script