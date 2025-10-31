import typing as t
from globus_cli.termio import env_interactive
import click
from shutil import get_terminal_size

class GlobusCommand(click.Command):
    """
    A custom command class which stores the special attributes
    of the form "adoc_*" with defaults of None. This lets us pass additional info to the
    adoc generator.

    It also automatically runs string formatting on command helptext to allow the
    inclusion of common strings (e.g. autoactivation help) and handles
    custom argument parsing.

    opts_to_combine is an interface for combining multiple options while preserving
    their original order. Given a dict of original option names as keys
    and combined option names as values, options are combined into a list of
    tuples of the original option name and value. For example:

    @command(
        ...
        opts_to_combine={
            "foo": "foo_bar",
            "bar": "foo_bar",
        },
    @click.option("--foo", multiple=True, expose_value=False)
    @click.option("--bar", multiple=True, expose_value=False)
    def example_command(*, foo_bar: list[tuple[Literal["foo", "bar"], Any]]):

        for option in foo_bar:
            original_option_name, value = option

    """

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        self.adoc_output = kwargs.pop('adoc_output', None)
        self.adoc_examples = kwargs.pop('adoc_examples', None)
        self.globus_disable_opts = kwargs.pop('globus_disable_opts', [])
        self.adoc_exit_status = kwargs.pop('adoc_exit_status', None)
        self.adoc_synopsis = kwargs.pop('adoc_synopsis', None)
        self.opts_to_combine = kwargs.pop('opts_to_combine', {})
        if 'context_settings' not in kwargs:
            kwargs['context_settings'] = {}
        if 'max_content_width' not in kwargs['context_settings']:
            try:
                cols = get_terminal_size(fallback=(80, 20)).columns
                content_width = cols if cols < 100 else int(0.8 * cols)
                kwargs['context_settings']['max_content_width'] = content_width
            except OSError:
                pass
        super().__init__(*args, **kwargs)

    def invoke(self, ctx: click.Context) -> t.Any:
        log.debug('command invoke start')
        try:
            env_interactive(raising=True)
            return super().invoke(ctx)
        finally:
            log.debug('command invoke exit')

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        had_args = bool(args)
        try:
            if self.opts_to_combine:
                combined_opts: dict[str, list[tuple[str, str]]] = {combined_name: [] for combined_name in self.opts_to_combine.values()}
                parser = self.make_parser(ctx)
                values, _, order = parser.parse_args(args=list(args))
                for opt in order:
                    if opt.name and opt.name in self.opts_to_combine:
                        value = values[opt.name].pop(0)
                        combined_name = self.opts_to_combine[opt.name]
                        combined_opts[combined_name].append((opt.name, value))
                ctx.params.update(combined_opts)
            return super().parse_args(ctx, args)
        except click.MissingParameter as e:
            if not had_args:
                click.secho(e.format_message(), fg='yellow', err=True)
                click.echo('\n' + ctx.get_help(), err=True)
                ctx.exit(2)
            raise