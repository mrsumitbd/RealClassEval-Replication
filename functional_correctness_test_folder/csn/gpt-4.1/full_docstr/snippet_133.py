
import argparse
from typing import Any


class DependenciesConfiguration:
    '''Dependency configuration class, for RuntimeContext.job_script_provider.'''

    def __init__(self, args: argparse.Namespace) -> None:
        '''Initialize.'''
        self.args = args

    def build_job_script(self, builder: 'Builder', command: list[str]) -> str:
        '''Use the galaxy-tool-util library to construct a build script.'''
        # Assume builder has a method build_script that takes command and args
        return builder.build_script(command, self.args)
