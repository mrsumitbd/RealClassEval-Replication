import click
import typing as t

class OneUseOption(click.Option):
    """
    Overwrites the type_cast_value function inherited from click.Parameter
    to assert an option was only used once, and then converts it back
    to the original value type.
    """

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)

    def has_explicit_annotation(self) -> bool:
        return True

    @property
    def type_annotation(self) -> type:
        from globus_cli.parsing.param_types import EndpointPlusPath
        if self.count:
            return bool
        if isinstance(self.type, EndpointPlusPath):
            return t.Union[self.type.get_type_annotation(self), None]
        raise NotImplementedError('OneUseOption requires a type annotation in this case.')

    def type_cast_value(self, ctx: click.Context, value: t.Any) -> t.Any:
        converted_val = super().type_cast_value(ctx, value)
        if self.multiple:
            if len(converted_val) > 1:
                raise click.BadParameter('Option used multiple times.', ctx=ctx)
            if len(converted_val):
                return converted_val[0]
            else:
                return None
        elif self.count:
            if converted_val > 1:
                raise click.BadParameter('Option used multiple times.', ctx=ctx)
            return bool(converted_val)
        else:
            raise ValueError('Internal error, OneUseOption expected either multiple or count, but got neither.')