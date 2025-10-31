import click

class ModelChoice(click.ParamType):
    """Custom click parameter type for selecting AI models.

    lgtm accepts a variety of AI models, and we show them in the usage of the CLI.
    However, we allow users to specify a custom model name as well.
    """
    name: str = 'model'
    choices: tuple[str, ...]

    def __init__(self, choices: tuple[str, ...]) -> None:
        self.choices = choices

    def convert(self, value: str, param: click.Parameter | None, ctx: click.Context | None) -> str:
        return value

    def get_metavar(self, param: click.Parameter, ctx: click.Context) -> str | None:
        return '[{}|<custom>]'.format('|'.join(self.choices))

    def get_choices(self, param: click.Parameter | None) -> tuple[str, ...]:
        return self.choices