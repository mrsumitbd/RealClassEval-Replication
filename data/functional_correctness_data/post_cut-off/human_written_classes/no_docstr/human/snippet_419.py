from lgtm_ai.base.schemas import IntOrNoLimit, PRSource, PRUrl
import click

class IntOrNoLimitType(click.ParamType):
    name = 'int-or-no-limit'

    def convert(self, value: str, param: click.Parameter | None, ctx: click.Context | None) -> IntOrNoLimit:
        if value == 'no-limit':
            return 'no-limit'
        try:
            return int(value)
        except (TypeError, ValueError):
            self.fail(f"{value!r} is not a valid integer or 'no-limit'", param, ctx)

    def get_metavar(self, param: click.Parameter, ctx: click.Context) -> str | None:
        return '[INTEGER|no-limit]'