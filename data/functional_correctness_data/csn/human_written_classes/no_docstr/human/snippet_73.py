import traceback
from textwrap import dedent
from attrs import define, field

@define
class _PrettyFormatter:
    _ERROR_MSG = dedent('        ===[{type}]===({path})===\n\n        {body}\n        -----------------------------\n        ')
    _SUCCESS_MSG = '===[SUCCESS]===({path})===\n'

    def filenotfound_error(self, path, exc_info):
        return self._ERROR_MSG.format(path=path, type='FileNotFoundError', body=f'{path!r} does not exist.')

    def parsing_error(self, path, exc_info):
        exc_type, exc_value, exc_traceback = exc_info
        exc_lines = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        return self._ERROR_MSG.format(path=path, type=exc_type.__name__, body=exc_lines)

    def validation_error(self, instance_path, error):
        return self._ERROR_MSG.format(path=instance_path, type=error.__class__.__name__, body=error)

    def validation_success(self, instance_path):
        return self._SUCCESS_MSG.format(path=instance_path)