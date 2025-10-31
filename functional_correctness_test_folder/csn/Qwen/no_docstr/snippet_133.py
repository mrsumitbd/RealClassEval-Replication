
import argparse


class DependenciesConfiguration:

    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args

    def build_job_script(self, builder: 'Builder', command: list[str]) -> str:
        script = builder.get_header()
        script += builder.set_environment_variables(self.args.env_vars)
        script += builder.install_dependencies(self.args.dependencies)
        script += builder.run_command(command)
        return script
