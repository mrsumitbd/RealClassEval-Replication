import click
from enum import Enum
import importlib

class Cli(click.MultiCommand):
    """Root MultiCommand for the semantic-release CLI"""

    class SubCmds(Enum):
        """Subcommand import definitions"""
        CHANGELOG = f'{__package__}.changelog'
        GENERATE_CONFIG = f'{__package__}.generate_config'
        VERSION = f'{__package__}.version'
        PUBLISH = f'{__package__}.publish'

    def list_commands(self, _ctx: click.Context) -> list[str]:
        return [subcmd.lower().replace('_', '-') for subcmd in Cli.SubCmds.__members__]

    def get_command(self, _ctx: click.Context, name: str) -> click.Command | None:
        subcmd_name = name.lower().replace('-', '_')
        try:
            subcmd_def: Cli.SubCmds = Cli.SubCmds.__dict__[subcmd_name.upper()]
            module_path = subcmd_def.value
            subcmd_module = importlib.import_module(module_path)
            return getattr(subcmd_module, subcmd_name)
        except (KeyError, ModuleNotFoundError, AttributeError):
            return None