
import argparse


class DependenciesConfiguration:
    '''Dependency configuration class, for RuntimeContext.job_script_provider.'''

    def __init__(self, args: argparse.Namespace) -> None:
        '''Initialize.'''
        self.args = args

    def build_job_script(self, builder: 'Builder', command: list[str]) -> str:
        script_lines = []
        # Add shebang if specified in args, else default to /bin/bash
        shebang = getattr(self.args, 'shebang', '#!/bin/bash')
        script_lines.append(shebang)
        script_lines.append('set -e')
        # Add dependency setup if specified
        dependencies = getattr(self.args, 'dependencies', [])
        for dep in dependencies:
            script_lines.append(f'source {dep}')
        # Add environment variables if specified
        env_vars = getattr(self.args, 'env', {})
        for k, v in env_vars.items():
            script_lines.append(f'export {k}="{v}"')
        # Add any pre-commands if specified
        pre_commands = getattr(self.args, 'pre_commands', [])
        for pre in pre_commands:
            script_lines.append(pre)
        # Add the main command
        script_lines.append(' '.join(command))
        # Add any post-commands if specified
        post_commands = getattr(self.args, 'post_commands', [])
        for post in post_commands:
            script_lines.append(post)
        return '\n'.join(script_lines)
