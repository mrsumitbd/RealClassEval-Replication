import click
import requests

class cli_api_error:
    """
    A decorator to catch HTTP errors for the command line.
    """

    def __init__(self, f):
        self.f = f
        self.__doc__ = f.__doc__

    def __call__(self, *args, **kwargs):
        try:
            return self.f(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            try:
                result = e.response.json()
                if 'errors' in result:
                    for error in result['errors']:
                        msg = error.get('message', 'Unknown error')
                elif 'title' in result:
                    msg = result['title']
                else:
                    msg = 'Unknown error'
            except ValueError:
                msg = f'Unable to parse {e.response.status_code} error as JSON: {e.response.text}'
        except InvalidAuthType as e:
            msg = 'This command requires application authentication, try passing --app-auth'
        except ValueError as e:
            msg = str(e)
        click.echo(click.style('⚡ ', fg='yellow') + click.style(msg, fg='red'), err=True)