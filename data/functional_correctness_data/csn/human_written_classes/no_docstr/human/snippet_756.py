import click
import textwrap

class AdocPage:

    def __init__(self, ctx) -> None:
        self.commandname = ctx.command_path
        self.short_help = ctx.command.get_short_help_str()
        self.description = textwrap.dedent(ctx.command.help).replace('\x08\n', '')
        self.synopsis = ctx.command.adoc_synopsis or self._format_synopsis(ctx)
        self.options = '\n\n'.join((_format_option(y[0]) + '\n' + y[1].replace('\n\n', '\n+\n') for y in [x.get_help_record(ctx) for x in ctx.command.params if isinstance(x, click.Option)] if y))
        self.output = ctx.command.adoc_output
        self.examples = ctx.command.adoc_examples
        uses_http = 'map_http_status' not in ctx.command.globus_disable_opts
        self.exit_status_text = ctx.command.adoc_exit_status or (EXIT_STATUS_TEXT if uses_http else EXIT_STATUS_NOHTTP_TEXT)

    def _format_synopsis(self, ctx):
        usage_pieces = ctx.command.collect_usage_pieces(ctx)
        as_str = ' '.join(usage_pieces)
        if as_str.endswith('...'):
            as_str = as_str[:-3]
        return f'`{self.commandname} {as_str}`'

    def __str__(self):
        sections = []
        sections.append(f'= {self.commandname.upper()}\n')
        sections.append(f'== NAME\n\n{self.commandname} - {self.short_help}\n')
        sections.append(f'== SYNOPSIS\n\n{self.synopsis}\n')
        if self.description:
            sections.append(f'== DESCRIPTION\n\n{self.description}\n')
        if self.options:
            sections.append(f'== OPTIONS\n{self.options}\n')
        if self.output:
            sections.append(f'== OUTPUT\n\n{self.output}\n')
        if self.examples:
            sections.append(f'== EXAMPLES\n\n{self.examples}\n')
        sections.append(f'== EXIT STATUS\n\n{self.exit_status_text}\n')
        return '\n'.join(sections)