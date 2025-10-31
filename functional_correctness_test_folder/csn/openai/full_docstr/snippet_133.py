
import argparse
from typing import List


class DependenciesConfiguration:
    '''Dependency configuration class, for RuntimeContext.job_script_provider.'''

    def __init__(self, args: argparse.Namespace) -> None:
        '''Initialize.'''
        self.args = args

    def build_job_script(self, builder: 'Builder', command: List[str]) -> str:
        '''Use the galaxy-tool-util library to construct a build script.'''
        # Import lazily to avoid unnecessary dependency import if not used
        from galaxy.tool_util.build import build_job_script as _build_job_script
        return _build_job_script(builder, command)
