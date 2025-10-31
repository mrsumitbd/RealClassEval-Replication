
import argparse
from galaxy.tool_util.deps import build_dependency_manager
from galaxy.tool_util.deps.dependencies import JobInfo
from galaxy.tool_util.deps.requirements import ToolRequirement


class DependenciesConfiguration:
    '''Dependency configuration class, for RuntimeContext.job_script_provider.'''

    def __init__(self, args: argparse.Namespace) -> None:
        '''Initialize.'''
        self.dependency_manager = build_dependency_manager(args)

    def build_job_script(self, builder: 'Builder', command: list[str]) -> str:
        '''Use the galaxy-tool-util library to construct a build script.'''
        job_info = JobInfo(
            working_directory=builder.job_working_directory,
            tool_directory=builder.tool_directory,
            job_directory=builder.job_directory,
            requirement_source=builder.requirements,
        )
        dependency_shell_commands = self.dependency_manager.dependency_shell_commands(
            job_info)
        return '\n'.join(dependency_shell_commands + command)
