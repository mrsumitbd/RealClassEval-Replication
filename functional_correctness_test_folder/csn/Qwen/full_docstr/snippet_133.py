
import argparse
from typing import List


class DependenciesConfiguration:
    '''Dependency configuration class, for RuntimeContext.job_script_provider.'''

    def __init__(self, args: argparse.Namespace) -> None:
        '''Initialize.'''
        self.args = args

    def build_job_script(self, builder: 'Builder', command: List[str]) -> str:
        '''Use the galaxy-tool-util library to construct a build script.'''
        from galaxy.tool_util.deps import build_dependency_script
        return build_dependency_script(builder, command, self.args)
