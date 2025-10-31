
class DependenciesConfiguration:

    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args

    def build_job_script(self, builder: 'Builder', command: list[str]) -> str:
        script = builder.build_script(command)
        return script
