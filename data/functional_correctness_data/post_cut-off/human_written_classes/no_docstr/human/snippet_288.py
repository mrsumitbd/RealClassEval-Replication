import click

class ControllerNeedeGroup(click.Group):

    def command(self, *args, **kwargs):

        def decorator(f):
            f = click.option('--controller-host', '-ch', required=True, help='The host of the controller')(f)
            f = click.option('--controller-port', '-cp', required=True, help='The port of the controller')(f)
            return super(ControllerNeedeGroup, self).command(*args, **kwargs)(f)
        return decorator